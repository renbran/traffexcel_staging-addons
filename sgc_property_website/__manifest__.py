# -*- coding: utf-8 -*-
{
    'name': 'SGC Property Website',
    'version': '19.0.1.0.0',
    'summary': 'Public property listings with carousel, gallery, and detail pages',
    'description': """
SGC Property Website
====================
Public-facing property portal built on Odoo Website.

Features:
- Featured property carousel on homepage
- Property listing grid with filters
- Individual property detail pages with photo gallery
- Search by location, type, price range
- Responsive design for mobile/tablet/desktop
- SEO-friendly URLs with slugs
- Links to construction.project records for tracked properties
    """,
    'category': 'Real Estate',
    'author': 'SGC',
    'website': 'https://sgc-tech.ai',
    'depends': ['website', 'sgc_construction_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/website_property_templates.xml',
        'views/website_property_views.xml',
        'data/property_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'sgc_property_website/static/src/css/property_website.css',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
