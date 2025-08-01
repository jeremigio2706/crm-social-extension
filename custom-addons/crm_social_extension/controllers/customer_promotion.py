# -*- coding: utf-8 -*-

import json
from odoo import http
from odoo.http import request


class CustomerPromotionController(http.Controller):

    @http.route('/customers', type='http', auth='public', website=True)
    def customer_promotion_page(self, search='', filter_type='', page=0, **kwargs):
        """Main customer promotion page"""
        customers_per_page = 12
        offset = int(page) * customers_per_page
        
        # Get customers for promotion
        Partner = request.env['res.partner']
        
        # Handle special filters
        if filter_type == 'complete' or search == 'complete_profile':
            domain = [
                '|', ('is_company', '=', True), ('is_company', '=', False),
                ('social_profile_complete', '=', True)
            ]
            customers = Partner.search(domain, limit=customers_per_page, offset=offset, order='name')
            total_found = Partner.search_count(domain)
            search = '' 
        elif filter_type == 'incomplete':
            domain = [
                '|', ('is_company', '=', True), ('is_company', '=', False),
                ('social_profile_complete', '=', False),
                '|', '|',
                ('facebook_url', '!=', False),
                ('linkedin_url', '!=', False),
                ('twitter_url', '!=', False)
            ]
            customers = Partner.search(domain, limit=customers_per_page, offset=offset, order='name')
            total_found = Partner.search_count(domain)
            search = '' 
        else:
            if search:
                domain = [
                    '|', ('is_company', '=', True), ('is_company', '=', False),
                    '|', ('name', 'ilike', search), ('email', 'ilike', search)
                ]
            else:
                domain = [
                    '|', ('is_company', '=', True), ('is_company', '=', False)
                ]
            customers = Partner.search(domain, limit=customers_per_page, offset=offset, order='name')
            total_found = Partner.search_count(domain)
        
        # Pagination logic
        has_next = (offset + customers_per_page) < total_found
        has_previous = offset > 0
        
        total_pages = (total_found + customers_per_page - 1) // customers_per_page
        current_page = int(page)
        
        stats = self._get_customer_stats()
        
        return request.render('crm_social_extension.customer_promotion_page', {
            'customers': customers,
            'search_term': search,
            'filter_type': filter_type,
            'current_page': current_page,
            'has_previous': has_previous,
            'has_next': has_next,
            'total_found': total_found,
            'total_pages': total_pages,
            'showing_start': offset + 1,
            'showing_end': min(offset + customers_per_page, total_found),
            **stats,
        })

    @http.route('/customers/search', type='json', auth='public', website=True)
    def customer_search_ajax(self, search='', limit=6, **kwargs):
        """AJAX endpoint for customer search suggestions"""
        Partner = request.env['res.partner']
        customers = Partner.search_customers_for_promotion(
            search_term=search,
            limit=limit
        )
        
        results = []
        for customer in customers:
            results.append({
                'id': customer.id,
                'name': customer.name,
                'image_url': f'/web/image/res.partner/{customer.id}/image_128' if customer.image_1920 else False,
                'website': customer.website,
                'social_complete': customer.social_profile_complete,
                'completion_rate': customer.social_profile_completion_rate,
                'social_media': customer.get_social_media_data(),
            })
        
        return {
            'customers': results,
            'total_found': len(results)
        }

    @http.route('/customers/<int:customer_id>', type='http', auth='public', website=True)
    def customer_detail(self, customer_id, **kwargs):
        """Individual customer detail page"""
        Partner = request.env['res.partner']
        customer = Partner.browse(customer_id)
        
        if not customer.exists():
            return request.not_found()

        values = {
            'customer': customer,
            'social_media': customer.get_social_media_data(),
        }
        
        return request.render('crm_social_extension.customer_detail_page', values)

    def _get_customer_stats(self):
        """Internal method to get customer statistics"""
        Partner = request.env['res.partner']
        
        all_customers = Partner.search([
            '|', ('is_company', '=', True), ('is_company', '=', False)
        ])
        
        complete_profiles = Partner.search([
            '|', ('is_company', '=', True), ('is_company', '=', False),
            ('social_profile_complete', '=', True)
        ])
        
        total_customers = len(all_customers)
        complete_count = len(complete_profiles)
        completion_rate = (complete_count / total_customers * 100) if total_customers > 0 else 0
        
        return {
            'total_customers': total_customers,
            'complete_profiles': complete_count,
            'completion_rate': completion_rate,
        }

    @http.route('/customers/stats', type='json', auth='public', website=True)
    def customer_stats(self, **kwargs):
        """Get customer statistics for dashboard"""
        return self._get_customer_stats()
