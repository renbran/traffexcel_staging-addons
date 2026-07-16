# -*- coding: utf-8 -*-
{
    "name": "SGC Construction - Analytic Enhanced",
    "version": "19.0.1.0.0",
    "summary": "Construction project analytic filtering, reporting & XLSX export",
    "description": "SGC Construction - Analytic Enhanced\n=====================================\nCombines analytic invoice filtering with project statement reporting.\n\nFeatures:\n- Adds computed Construction Project field on invoices, bills & journal items\n- Project Invoices, Project Bills, Project Credit Notes, Project Journal Items menu actions\n- Group-by Project & search filters on all invoice/bill list views\n- Smart button on invoice form to open linked Construction Project\n- Analytic line search/filter by Construction Project\n- Project Statement (XLSX) download wizard with summary + detail sheets",
    "category": "Construction/Accounting",
    "author": "SGC TECH AI",
    "website": "https://sgc-tech.ai",
    "license": "OPL-1",
    "depends": [
        "account",
        "analytic",
        "sgc_construction_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/account_move_views.xml",
        "views/analytic_report_views.xml",
        "views/project_statement_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
