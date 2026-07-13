# -*- coding: utf-8 -*-
{
    'name': 'SGC Save/Discard Highlight',
    'version': '19.0.1.0.0',
    'category': 'Hidden',
    'summary': 'Make Save and Discard buttons stand out across the backend',
    'description': """
SGC Save/Discard Highlight
===========================
Gives the form Save and Discard controls a distinct, high-contrast style
(solid colors, clear icons, a subtle attention animation while there are
unsaved changes) so they read as prominent, unmistakable actions on every
form view in the database, regardless of which backend theme is active.
    """,
    'author': 'SGC',
    'website': 'https://sgc-tech.ai',
    'license': 'LGPL-3',
    'depends': ['web'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'sgc_save_discard_highlight/static/src/scss/save_discard_highlight.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
