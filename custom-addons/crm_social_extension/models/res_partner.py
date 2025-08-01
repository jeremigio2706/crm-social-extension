# -*- coding: utf-8 -*-

from odoo import models, fields, api
import re
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Social Media Fields
    facebook_url = fields.Char(
        string='Facebook URL',
        help='Facebook profile or page URL'
    )
    linkedin_url = fields.Char(
        string='LinkedIn URL',
        help='LinkedIn profile URL'
    )
    twitter_url = fields.Char(
        string='X URL',
        help='X (formerly Twitter) profile URL'
    )
    
    # Computed field for profile completion
    social_profile_complete = fields.Boolean(
        string='Social Profile Complete',
        compute='_compute_social_profile_complete',
        store=True,
        help='True if all social media URLs are filled'
    )
    
    social_profile_completion_rate = fields.Float(
        string='Profile Completion Rate',
        compute='_compute_social_profile_completion_rate',
        store=True,
        help='Percentage of completed social media fields (0-1 for percentage widget)'
    )
    
    social_profile_completion_display = fields.Char(
        string='% Completado',
        compute='_compute_social_profile_completion_rate',
        store=True,
        help='Formatted percentage display for views'
    )

    @api.depends('facebook_url', 'linkedin_url', 'twitter_url')
    def _compute_social_profile_complete(self):
        """Compute if social profile is complete (all social URLs filled)"""
        for partner in self:
            partner.social_profile_complete = bool(
                partner.facebook_url and 
                partner.linkedin_url and 
                partner.twitter_url
            )

    @api.depends('facebook_url', 'linkedin_url', 'twitter_url')
    def _compute_social_profile_completion_rate(self):
        """Compute the completion rate percentage and display"""
        for partner in self:
            filled_fields = 0
            total_fields = 3
            
            if partner.facebook_url:
                filled_fields += 1
            if partner.linkedin_url:
                filled_fields += 1
            if partner.twitter_url:
                filled_fields += 1
                
            partner.social_profile_completion_rate = filled_fields / total_fields
            
            percentage = (filled_fields / total_fields) * 100
            if percentage == 100:
                partner.social_profile_completion_display = "100%"
            elif percentage == 0:
                partner.social_profile_completion_display = "0%"
            else:
                partner.social_profile_completion_display = f"{percentage:.1f}%"

    def _validate_social_url(self, url, platform):
        """Validate social media URL format"""
        if not url:
            return True
            
        patterns = {
            'facebook': r'^https?://(www\.)?(facebook\.com|fb\.com)/.+',
            'linkedin': r'^https?://(www\.)?linkedin\.com/.+',
            'twitter': r'^https?://(www\.)?(twitter\.com|x\.com)/.+'
        }
        
        pattern = patterns.get(platform)
        if pattern and not re.match(pattern, url, re.IGNORECASE):
            return False
        return True

    @api.constrains('facebook_url')
    def _check_facebook_url(self):
        """Validate Facebook URL format"""
        for partner in self:
            if not self._validate_social_url(partner.facebook_url, 'facebook'):
                raise models.ValidationError(
                    'Please enter a valid Facebook URL (e.g., https://facebook.com/username)'
                )

    @api.constrains('linkedin_url')
    def _check_linkedin_url(self):
        """Validate LinkedIn URL format"""
        for partner in self:
            if not self._validate_social_url(partner.linkedin_url, 'linkedin'):
                raise models.ValidationError(
                    'Please enter a valid LinkedIn URL (e.g., https://linkedin.com/in/username)'
                )

    @api.constrains('twitter_url')
    def _check_twitter_url(self):
        """Validate X URL format"""
        for partner in self:
            if not self._validate_social_url(partner.twitter_url, 'twitter'):
                raise models.ValidationError(
                    'Please enter a valid X URL (e.g., https://x.com/username)'
                )

    def get_social_media_data(self):
        """Get formatted social media data for website display"""
        social_data = []
        
        if self.facebook_url:
            social_data.append({
                'platform': 'facebook',
                'url': self.facebook_url,
                'icon': 'fa-facebook',
                'name': 'Facebook',
                'color': '#1877f2'
            })
            
        if self.linkedin_url:
            social_data.append({
                'platform': 'linkedin',
                'url': self.linkedin_url,
                'icon': 'fa-linkedin',
                'name': 'LinkedIn',
                'color': '#0077b5'
            })
            
        if self.twitter_url:
            social_data.append({
                'platform': 'twitter',
                'url': self.twitter_url,
                'icon': 'fa-twitter',
                'name': 'X',
                'color': '#000000'
            })
            
        return social_data

    @api.model
    def search_customers_for_promotion(self, search_term='', limit=None):
        """Search customers with social media for website promotion page"""
        domain = [
            '|', '|',
            ('facebook_url', '!=', False),
            ('linkedin_url', '!=', False),
            ('twitter_url', '!=', False)
        ]
        
        if search_term:
            search_domain = [
                '|', '|', '|', '|',
                ('name', 'ilike', search_term),
                ('facebook_url', 'ilike', search_term),
                ('linkedin_url', 'ilike', search_term),
                ('twitter_url', 'ilike', search_term),
                ('website', 'ilike', search_term)
            ]
            domain = expression.AND([domain, search_domain])
        
        return self.search(domain, limit=limit, order='social_profile_complete desc, name')

    def action_open_social_profiles(self):
        """Action to open all social profiles in new tabs"""
        return {
            'type': 'ir.actions.act_url',
            'url': self.facebook_url or self.linkedin_url or self.twitter_url,
            'target': 'new',
        }
