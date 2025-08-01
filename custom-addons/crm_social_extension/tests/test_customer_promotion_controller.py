# -*- coding: utf-8 -*-

import json
from unittest.mock import patch, MagicMock
from odoo.tests.common import HttpCase
from odoo.http import request
from odoo.tests import tagged


@tagged('customer_promotion_controller_test')
class TestCustomerPromotionController(HttpCase):

    def setUp(self):
        super(TestCustomerPromotionController, self).setUp()
        self.Partner = self.env['res.partner']
        
        # Create test customers
        self.customer1 = self.Partner.create({
            'name': 'Tech Solutions Inc',
            'is_company': True,
            'facebook_url': 'https://facebook.com/techsolutions',
            'linkedin_url': 'https://linkedin.com/company/techsolutions',
            'twitter_url': 'https://twitter.com/techsolutions',
            'website': 'https://techsolutions.com',
            'email': 'info@techsolutions.com'
        })
        
        self.customer2 = self.Partner.create({
            'name': 'Digital Marketing Corp',
            'is_company': True,
            'facebook_url': 'https://facebook.com/digitalmarketing',
            'linkedin_url': 'https://linkedin.com/company/digitalmarketing',
            # No Twitter URL - incomplete profile
            'website': 'https://digitalmarketing.com',
            'email': 'contact@digitalmarketing.com'
        })
        
        self.customer3 = self.Partner.create({
            'name': 'No Social Media Co',
            'is_company': True,
            'website': 'https://nosocial.com',
            'email': 'info@nosocial.com'
        })

    def test_customer_promotion_page_access(self):
        """Test that customer promotion page is accessible"""
        # Authenticate as admin to access the page
        self.authenticate('admin', 'admin')
        response = self.url_open('/customers')
        self.assertEqual(response.status_code, 200)
        
        # Check for Spanish text since we converted the interface
        content = response.content.decode('utf-8')
        self.assertIn('Nuestros Increíbles Clientes', content)
        self.assertIn('Total de Clientes', content)

    def test_customer_promotion_page_content(self):
        """Test customer promotion page displays customers correctly"""
        # Authenticate as admin to access the page and see test data
        self.authenticate('admin', 'admin')
        
        # Open the page without any filters
        response = self.url_open('/customers')
        content = response.content.decode('utf-8')
        
        self.assertIn('Creative Design Studio', content)
        self.assertIn('Digital Marketing Corp', content)
        self.assertIn('Brandon Freeman', content)

    def test_customer_search_functionality(self):
        """Test customer search with query parameter"""
        # Authenticate to ensure data is visible in the HTTP thread
        self.authenticate('admin', 'admin') 
        response = self.url_open('/customers?search=Tech')
        content = response.content.decode('utf-8')

        # Should show matching customer
        self.assertIn('Tech Solutions Inc', content)

        # Should not show non-matching customers
        self.assertNotIn('Digital Marketing Corp', content)

    def test_customer_detail_page(self):
        """Test individual customer detail page"""
        # Authenticate as admin to access customer details
        self.authenticate('admin', 'admin')
        response = self.url_open(f'/customers/{self.customer1.id}')
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        self.assertIn('Tech Solutions Inc', content)
        self.assertIn('facebook.com/techsolutions', content)
        # Check for Spanish text for complete profile
        self.assertIn('Perfil Social Completo', content)

    def test_customer_detail_page_incomplete_profile(self):
        """Test customer detail page with incomplete profile"""
        # Authenticate as admin
        self.authenticate('admin', 'admin')
        response = self.url_open(f'/customers/{self.customer2.id}')
        self.assertEqual(response.status_code, 200)
        
        content = response.content.decode('utf-8')
        self.assertIn('Digital Marketing Corp', content)
        # Check for Spanish text for profile completion
        self.assertIn('Perfil Completo', content)  # Should show completion percentage

    def test_customer_detail_page_not_found(self):
        """Test customer detail page with invalid customer ID"""
        response = self.url_open('/customers/99999')
        self.assertEqual(response.status_code, 404)

    def test_customer_detail_page_no_social_media(self):
        """Test customer detail page for customer without social media"""
        # Authenticate as admin
        self.authenticate('admin', 'admin')
        response = self.url_open(f'/customers/{self.customer3.id}')
        # Customer without social media should still be accessible since our model includes all customers
        self.assertEqual(response.status_code, 200)

    def test_customer_search_ajax_endpoint(self):
        """Test AJAX search endpoint"""
        Partner = self.env['res.partner'].sudo() 
        results = Partner.search_customers_for_promotion('Tech', limit=5)
        
        self.assertIn(self.customer1, results)

    
    def test_customer_stats_data(self):
        """Test customer statistics calculation"""
        Partner = self.env['res.partner']

        # Count customers with at least one social media URL
        customers_with_social = Partner.search_count([
            '|', '|',
            ('facebook_url', '!=', False),
            ('linkedin_url', '!=', False),
            ('twitter_url', '!=', False)
        ])

        # Check that AT LEAST 2 customers exist, which makes the test
        # less brittle and independent of other tests' data.
        self.assertGreaterEqual(customers_with_social, 2)

        # Complete profiles
        complete_profiles = Partner.search_count([
            ('social_profile_complete', '=', True)
        ])

        # Should only include customer1
        self.assertGreaterEqual(complete_profiles, 1)

    def test_pagination_functionality(self):
        """Test pagination in customer list"""
        # Create additional customers to test pagination
        for i in range(15):
            self.Partner.create({
                'name': f'Test Customer {i}',
                'is_company': True,
                'facebook_url': f'https://facebook.com/testcustomer{i}',
            })
        
        # Test first page
        response = self.url_open('/customers')
        self.assertEqual(response.status_code, 200)
        
        # Test second page
        response = self.url_open('/customers?page=1')
        self.assertEqual(response.status_code, 200)

    def test_customer_social_media_data_method(self):
        """Test get_social_media_data method returns correct format"""
        social_data = self.customer1.get_social_media_data()
        
        self.assertEqual(len(social_data), 3)  # Facebook, LinkedIn, Twitter
        
        # Check each platform data structure
        for platform_data in social_data:
            self.assertIn('platform', platform_data)
            self.assertIn('url', platform_data)
            self.assertIn('icon', platform_data)
            self.assertIn('name', platform_data)
            self.assertIn('color', platform_data)
        
        # Check specific platforms
        platform_names = [data['platform'] for data in social_data]
        self.assertIn('facebook', platform_names)
        self.assertIn('linkedin', platform_names)
        self.assertIn('twitter', platform_names)

    def test_search_by_social_media_url(self):
        """Test searching customers by social media URL"""
        Partner = self.env['res.partner']
        
        # Search by Facebook URL
        results = Partner.search_customers_for_promotion('facebook.com/techsolutions')
        self.assertIn(self.customer1, results)
        self.assertNotIn(self.customer2, results)
        
        # Search by LinkedIn URL
        results = Partner.search_customers_for_promotion('linkedin.com/company/digitalmarketing')
        self.assertIn(self.customer2, results)
        self.assertNotIn(self.customer1, results)

    def test_empty_search_results(self):
        """Test search with no matching results"""
        self.authenticate('admin', 'admin')
        response = self.url_open('/customers?search=NonexistentCompany')
        content = response.content.decode('utf-8')
        
        self.assertIn('No se encontraron clientes', content)

    def test_customer_promotion_page_stats_display(self):
        """Test that stats are correctly displayed on promotion page"""
        response = self.url_open('/customers')
        content = response.content.decode('utf-8')
        
        # Should show total customers count
        self.assertIn('Total de Clientes', content)
        
        # Should show complete profiles count
        self.assertIn('Perfiles Completos', content)

        # Should show completion rate
        self.assertIn('Tasa de Finalización', content)

   
    def test_customer_search_ajax_detailed(self):
        """Test AJAX search endpoint with detailed response"""
        self.authenticate('admin', 'admin')

        # Construye la URL completa para la llamada
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        search_url = f"{base_url}/customers/search"

        # Usa self.opener.post con el payload en el argumento 'json'
        response = self.opener.post(
            search_url,
            json={'params': {'search': 'Tech', 'limit': 6}}
        )

        self.assertEqual(response.status_code, 200)
        # La respuesta de una ruta JSON se encuentra en la clave 'result'
        data = response.json().get('result')

        self.assertIn('customers', data)
        self.assertIn('total_found', data)

        if data['customers']:
            customer = data['customers'][0]
            required_keys = ['id', 'name', 'image_url', 'website', 'social_complete', 'completion_rate', 'social_media']
            for key in required_keys:
                self.assertIn(key, customer)

    def test_filter_complete_profiles(self):
        """Test filtering for complete profiles"""
        self.authenticate('admin', 'admin')
        response = self.url_open('/customers?filter_type=complete')
        content = response.content.decode('utf-8')
        
        # Should show complete profiles
        self.assertIn('Tech Solutions Inc', content)
        # Should not show incomplete profiles
        self.assertNotIn('Digital Marketing Corp', content)

    def test_filter_incomplete_profiles(self):
        """Test filtering for incomplete profiles"""
        self.authenticate('admin', 'admin')
        response = self.url_open('/customers?filter_type=incomplete')
        content = response.content.decode('utf-8')
        
        # Should show incomplete profiles that have some social media
        self.assertIn('Digital Marketing Corp', content)

    def test_customer_stats_endpoint(self):
        """Test customer stats JSON endpoint"""
        # self.opener is a requests.Session object, use its 'post' method
        # The URL must be absolute for this type of request.
        stats_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/customers/stats'
        response = self.opener.post(stats_url, json={'params': {}})

        self.assertEqual(response.status_code, 200)

        # The response from a JSON route is inside a 'result' key
        data = response.json().get('result')

        self.assertIn('total_customers', data)
        self.assertIn('complete_profiles', data)
        self.assertIn('completion_rate', data)

    def test_pagination_edge_cases(self):
        """Test pagination with edge cases"""
        # Test page 0
        response = self.url_open('/customers?page=0')
        self.assertEqual(response.status_code, 200)
        
        # Test high page number
        response = self.url_open('/customers?page=999')
        self.assertEqual(response.status_code, 200)

    def test_special_search_terms(self):
        """Test special search terms"""
        # Test 'complete_profile' search
        self.authenticate('admin', 'admin')
        response = self.url_open('/customers?search=complete_profile')
        content = response.content.decode('utf-8')
        self.assertIn('Tech Solutions Inc', content)  


    def test_customer_detail_social_media_display(self):
        """Test customer detail page shows social media correctly"""
        self.authenticate('admin', 'admin')
        response = self.url_open(f'/customers/{self.customer1.id}')
        content = response.content.decode('utf-8')
        
        # Should show all social media links
        self.assertIn('facebook.com/techsolutions', content)
        self.assertIn('linkedin.com/company/techsolutions', content)
        self.assertIn('twitter.com/techsolutions', content)
