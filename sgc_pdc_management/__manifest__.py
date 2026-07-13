# -*- coding: utf-8 -*-
{
    'name': 'SGC PDC & Bank Guarantee Management',
    'version': '19.0.1.0.1',
    'summary': 'Post-Dated Cheque, Bank Guarantee & Performance Bond tracking for UAE construction',
    'description': """
SGC PDC & Bank Guarantee Management
=====================================
Extends account.payment (no Odoo core files modified) to track:
- Customer PDC received
- Vendor PDC issued
- Bank Guarantees (BG)
- Performance Bonds

Features:
- Full state workflow: Draft → Received/Issued → Deposited → Cleared | Bounced
- Printable A4 PDC slip / BG register
- PDC ageing report
- Integration with construction.project
- UAE-style layout with cheque details
    """,
    'category': 'Accounting/Construction',
    'author': 'SGC',
    'website': 'https://sgc-tech.ai',
    'depends': ['account', 'sgc_construction_management'],
    'data': [
        'security/ir.model.access.csv',
        'data/pdc_sequence.xml',
        'views/pdc_payment_views.xml',
        'views/pdc_menus.xml',
        'report/pdc_report.xml',
        'report/pdc_report_template.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'sgc_pdc_management/static/src/css/pdc_report.css',
        ],
    },
    'application': False,
    'installable': True,
    'license': 'OPL-1',
}
