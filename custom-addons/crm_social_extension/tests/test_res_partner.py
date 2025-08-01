# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged


@tagged('res_partner_test')
class TestResPartner(TransactionCase):

    def setUp(self):
        super(TestResPartner, self).setUp()
        self.Partner = self.env['res.partner']
        
        # Create test customers
        self.customer_complete = self.Partner.create({
            'name': 'Complete Customer',
            'is_company': True,
            'facebook_url': 'https://facebook.com/completecustomer',
            'linkedin_url': 'https://linkedin.com/company/completecustomer',
            'twitter_url': 'https://twitter.com/completecustomer',
            'email': 'complete@customer.com',
            'website': 'https://completecustomer.com'
        })
        
        self.customer_partial = self.Partner.create({
            'name': 'Partial Customer',
            'is_company': True,
            'facebook_url': 'https://facebook.com/partialcustomer',
            'linkedin_url': 'https://linkedin.com/company/partialcustomer',
            # No Twitter URL
            'email': 'partial@customer.com'
        })
        
        self.customer_empty = self.Partner.create({
            'name': 'Empty Customer',
            'is_company': True,
            'email': 'empty@customer.com'
        })

    def test_social_profile_complete_computation(self):
        """Test social profile completion computation"""
        # Complete profile should be True
        self.assertTrue(
            self.customer_complete.social_profile_complete,
            "Customer with all social URLs should have complete profile"
        )
        
        # Partial profile should be False
        self.assertFalse(
            self.customer_partial.social_profile_complete,
            "Customer with missing social URLs should not have complete profile"
        )
        
        # Empty profile should be False
        self.assertFalse(
            self.customer_empty.social_profile_complete,
            "Customer with no social URLs should not have complete profile"
        )

    def test_social_profile_completion_rate(self):
        """Test social profile completion rate calculation"""
        # Complete profile should be 1.0 (100%)
        self.assertEqual(
            self.customer_complete.social_profile_completion_rate,
            1.0,
            "Complete profile should have 1.0 completion rate (100%)"
        )
        
        # Partial profile should be 0.6667 (2 out of 3)
        self.assertAlmostEqual(
            self.customer_partial.social_profile_completion_rate,
            0.6667,
            places=3,
            msg="Partial profile should have ~0.6667 completion rate (66.67%)"
        )
        
        # Empty profile should be 0.0
        self.assertEqual(
            self.customer_empty.social_profile_completion_rate,
            0.0,
            "Empty profile should have 0.0 completion rate (0%)"
        )

    def test_facebook_url_validation(self):
        """Test Facebook URL validation"""
        # Valid URLs should pass
        valid_urls = [
            'https://facebook.com/username',
            'https://www.facebook.com/username',
            'http://facebook.com/pages/company',
            'https://fb.com/username'
        ]
        
        for url in valid_urls:
            customer = self.Partner.create({
                'name': f'Test Customer {url}',
                'facebook_url': url
            })
            self.assertEqual(customer.facebook_url, url)

        # Invalid URLs should raise ValidationError
        invalid_urls = [
            'https://linkedin.com/username',
            'https://twitter.com/username',
            'not-a-url',
            'https://example.com/facebook'
        ]
        
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                self.Partner.create({
                    'name': f'Test Customer Invalid {url}',
                    'facebook_url': url
                })

    def test_linkedin_url_validation(self):
        """Test LinkedIn URL validation"""
        # Valid URLs should pass
        valid_urls = [
            'https://linkedin.com/in/username',
            'https://www.linkedin.com/company/company-name',
            'http://linkedin.com/in/username'
        ]
        
        for url in valid_urls:
            customer = self.Partner.create({
                'name': f'Test Customer {url}',
                'linkedin_url': url
            })
            self.assertEqual(customer.linkedin_url, url)

        # Invalid URLs should raise ValidationError
        invalid_urls = [
            'https://facebook.com/username',
            'https://twitter.com/username',
            'not-a-url'
        ]
        
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                self.Partner.create({
                    'name': f'Test Customer Invalid {url}',
                    'linkedin_url': url
                })

    def test_twitter_url_validation(self):
        """Test Twitter URL validation"""
        # Valid URLs should pass
        valid_urls = [
            'https://twitter.com/username',
            'https://www.twitter.com/username',
            'http://twitter.com/username',
            'https://x.com/username'
        ]
        
        for url in valid_urls:
            customer = self.Partner.create({
                'name': f'Test Customer {url}',
                'twitter_url': url
            })
            self.assertEqual(customer.twitter_url, url)

        # Invalid URLs should raise ValidationError
        invalid_urls = [
            'https://facebook.com/username',
            'https://linkedin.com/username',
            'not-a-url'
        ]
        
        for url in invalid_urls:
            with self.assertRaises(ValidationError):
                self.Partner.create({
                    'name': f'Test Customer Invalid {url}',
                    'twitter_url': url
                })

    def test_get_social_media_data(self):
        """Test social media data formatting"""
        social_data = self.customer_complete.get_social_media_data()
        
        # Should return 3 social platforms
        self.assertEqual(len(social_data), 3)
        
        # Check platform names
        platform_names = [data['platform'] for data in social_data]
        self.assertIn('facebook', platform_names)
        self.assertIn('linkedin', platform_names)
        self.assertIn('twitter', platform_names)
        
        # Check data structure
        for data in social_data:
            self.assertIn('platform', data)
            self.assertIn('url', data)
            self.assertIn('icon', data)
            self.assertIn('name', data)
            self.assertIn('color', data)

    def test_search_customers_for_promotion(self):
        """Test customer search for promotion page"""
        # Search without term should return ALL customers (with or without social media)
        all_customers = self.Partner.search_customers_for_promotion()
        self.assertIn(self.customer_complete, all_customers)
        self.assertIn(self.customer_partial, all_customers)
        self.assertNotIn(self.customer_empty, all_customers)
        
        # Search by name
        name_results = self.Partner.search_customers_for_promotion('Complete')
        self.assertIn(self.customer_complete, name_results)
        self.assertNotIn(self.customer_partial, name_results)
        
        # Search by social media URL
        social_results = self.Partner.search_customers_for_promotion('facebook.com/completecustomer')
        self.assertIn(self.customer_complete, social_results)
        self.assertNotIn(self.customer_partial, social_results)

    def test_profile_completion_changes(self):
        """Test that completion status updates when URLs change"""
        # Start with incomplete profile
        self.assertFalse(self.customer_partial.social_profile_complete)
        
        # Add missing Twitter URL
        self.customer_partial.twitter_url = 'https://twitter.com/partialcustomer'
        
        # Should now be complete
        self.assertTrue(self.customer_partial.social_profile_complete)
        self.assertEqual(self.customer_partial.social_profile_completion_rate, 1.0)
        
        # Remove a URL
        self.customer_partial.facebook_url = False
        
        # Should be incomplete again
        self.assertFalse(self.customer_partial.social_profile_complete)
        self.assertAlmostEqual(self.customer_partial.social_profile_completion_rate, 0.6667, places=3)

    def test_url_validation_edge_cases(self):
        """Test URL validation edge cases"""
        # Empty URLs should be valid (not required)
        customer = self.Partner.create({
            'name': 'Test Customer Empty URLs',
            'facebook_url': '',
            'linkedin_url': '',
            'twitter_url': ''
        })
        self.assertEqual(customer.social_profile_completion_rate, 0.0)
        
        # False values should be valid
        customer = self.Partner.create({
            'name': 'Test Customer False URLs',
            'facebook_url': False,
            'linkedin_url': False,
            'twitter_url': False
        })
        self.assertEqual(customer.social_profile_completion_rate, 0.0)

    def test_company_vs_individual_filter(self):
        """Test that both companies and individuals are included in promotion search"""
        # Create individual contact
        individual = self.Partner.create({
            'name': 'Individual Contact',
            'is_company': False,
            'facebook_url': 'https://facebook.com/individual',
            'linkedin_url': 'https://linkedin.com/in/individual',
            'twitter_url': 'https://twitter.com/individual'
        })
        
        # Search should include BOTH individual contacts AND companies
        customers = self.Partner.search_customers_for_promotion()
        self.assertIn(individual, customers)  # Individual should be included
        self.assertIn(self.customer_complete, customers)  # Company should be included

    def test_action_open_social_profiles(self):
        """Test action to open social profiles"""
        action = self.customer_complete.action_open_social_profiles()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertEqual(action['target'], 'new')
        self.assertIn('facebook.com', action['url'])

    def test_social_profile_completion_display_formatting(self):
        """Test completion display formatting"""
        # Test 100%
        self.assertEqual(self.customer_complete.social_profile_completion_display, "100%")
        
        # Test 0%
        self.assertEqual(self.customer_empty.social_profile_completion_display, "0%")
        
        # Test partial (66.7%)
        self.assertEqual(self.customer_partial.social_profile_completion_display, "66.7%")

    def test_validate_social_url_method(self):
        """Test internal URL validation method"""
        # Test Facebook validation
        self.assertTrue(self.customer_complete._validate_social_url('https://facebook.com/test', 'facebook'))
        self.assertFalse(self.customer_complete._validate_social_url('https://linkedin.com/test', 'facebook'))
        
        # Test LinkedIn validation
        self.assertTrue(self.customer_complete._validate_social_url('https://linkedin.com/in/test', 'linkedin'))
        self.assertFalse(self.customer_complete._validate_social_url('https://facebook.com/test', 'linkedin'))
        
        # Test Twitter validation
        self.assertTrue(self.customer_complete._validate_social_url('https://x.com/test', 'twitter'))
        self.assertFalse(self.customer_complete._validate_social_url('https://facebook.com/test', 'twitter'))

    def test_search_customers_ordering(self):
        """Test that search results are ordered correctly"""
        results = self.Partner.search_customers_for_promotion()
        complete_customers = [c for c in results if c.social_profile_complete]
        incomplete_customers = [c for c in results if not c.social_profile_complete]
        
        if complete_customers and incomplete_customers:
            first_complete_index = list(results).index(complete_customers[0])
            first_incomplete_index = list(results).index(incomplete_customers[0])
            self.assertLess(first_complete_index, first_incomplete_index)

    def test_social_media_data_colors_and_icons(self):
        """Test social media data includes correct colors and icons"""
        social_data = self.customer_complete.get_social_media_data()
        
        facebook_data = next(d for d in social_data if d['platform'] == 'facebook')
        self.assertEqual(facebook_data['color'], '#1877f2')
        self.assertEqual(facebook_data['icon'], 'fa-facebook')
        
        linkedin_data = next(d for d in social_data if d['platform'] == 'linkedin')
        self.assertEqual(linkedin_data['color'], '#0077b5')
        self.assertEqual(linkedin_data['icon'], 'fa-linkedin')
        
        twitter_data = next(d for d in social_data if d['platform'] == 'twitter')
        self.assertEqual(twitter_data['color'], '#000000')
        self.assertEqual(twitter_data['icon'], 'fa-twitter')