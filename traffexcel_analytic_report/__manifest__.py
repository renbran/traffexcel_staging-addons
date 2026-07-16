# -*- coding: utf-8 -*-
{
    'name': 'Traffexcel Analytic Report - Construction Projects',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Analytic report predefined by Construction Project + Project Statement XLSX export',
    'depends': ['account', 'analytic'],
    'data': [
        'security/ir.model.access.csv',
        'views/analytic_report_views.xml',
        'views/project_statement_wizard_views.xml',
    ],
    'installable': False,
    'license': 'LGPL-3',
}
