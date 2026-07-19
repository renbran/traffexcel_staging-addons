{
    'name': 'SGC TECH AI Enterprise Theme',
    'version': '19.0.1.0.0',
    'sequence': 7,
    'summary': 'SGC TECH AI Corporate Theme for Odoo',
    "author": "SGC TECH AI",
    'license': 'LGPL-3',
    'maintainer': 'SGC TECH AI',
    "company": "SGC TECH AI",
    'website': 'https://sgctech.ai',
    'depends': [
        'web'
    ],
    'category': 'Branding',
    'description': """
        SGC TECH AI Enterprise Theme
        A premium corporate theme for Odoo v19, designed to reflect the
        architectural precision and institutional authority of the SGC TECH AI brand.
        Built in Dubai. Designed for the world.
    """,
    'assets': {
        'web.assets_backend': [
            ('prepend', '/sgc_tech_ai_theme/static/src/scss/primary_variables_custom.scss'),
            '/sgc_tech_ai_theme/static/src/scss/secondary_variables.scss',
            '/sgc_tech_ai_theme/static/src/scss/fields_extra_custom.scss',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/icon.png'],
}