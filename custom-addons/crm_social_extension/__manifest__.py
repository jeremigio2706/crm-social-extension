# -*- coding: utf-8 -*-
{
    'name': 'CRM Social Extension',
    'version': '18.0.1.0.0',
    'category': 'Customer Relationship Management',
    'summary': 'Enhance CRM with social media integration and customer promotion',
    'description': """
CRM Social Extension
====================

This module extends the CRM functionality to include:

Features:
---------
* Social media URL registration for customers (Facebook, LinkedIn, Twitter)
* Visual indicators for complete/incomplete customer profiles
* Customer promotion website page with social media integration
* Advanced search functionality by name and social accounts
* Profile completion tracking and filtering

Technical:
----------
* Unit tests with coverage reporting
* Clean Git workflow
* Modern web interface
* Responsive design

Author: Jorge Ernesto Remigio Carrera
License: AGPL-3
    """,
    'author': 'Jorge Ernesto Remigio Carrera',
    'website': 'https://github.com/jeremigio2706/crm-social-extension',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'crm',
        'website',
        'contacts',
    ],
    'data': [
        'views/res_partner_views.xml',
        'views/website_customer_promotion.xml',
        'data/website_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'crm_social_extension/static/src/css/social_extension.css',
            'crm_social_extension/static/src/js/social_widget.js',
        ],
        'web.assets_frontend': [
            'crm_social_extension/static/src/css/website_customer_promotion.css',
            'crm_social_extension/static/src/js/customer_search.js',
        ],
    },
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': False,
    'external_dependencies': {
        'python': [],
    },
    'images': ['static/description/icon.png'],
    'sequence': 1,
}
