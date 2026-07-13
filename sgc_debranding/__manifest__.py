{
    'name': 'SGC Debranding',
    'version': '19.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Replace Odoo marketing content with SGC branding',
    'author': 'SGC Construction',
    'license': 'LGPL-3',
    'depends': ['web', 'mail', 'auth_signup', 'portal', 'digest'],
    'data': [
        'views/webclient_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
