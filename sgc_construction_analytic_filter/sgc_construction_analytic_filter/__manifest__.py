# -*- coding: utf-8 -*-
{
    'name': 'SGC Construction - Analytic Invoice Filter',
    'version': '19.0.1.0.0',
    'summary': 'Filter and group invoices/bills by construction project analytic account',
    'description': """
SGC Construction - Analytic Invoice Filter
===========================================
Extends Accounting invoices and bills with construction project filtering:

- Adds a computed 'Construction Project' field on invoices/bills
- Automatically detects the project from analytic distribution on invoice lines
- Provides pre-filtered actions: Project Invoices, Project Bills
- Group-by Project available on all invoice/bill list views
- Quick filter shortcuts in the Accounting menu
    """,
    'category': 'Construction/Accounting',
    'author': 'SGC TECH AI',
    'website': 'https://sgc-tech.ai',
    'depends': ['account', 'sgc_construction_management'],
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}
