# -*- coding: utf-8 -*-
{
    'name': 'SGC Mock Property Portal API',
    'version': '19.0.1.0.0',
    'summary': 'Mock REST API for property portal testing (Bayut/PropertyFinder style)',
    'description': """
SGC Mock Property Portal API
==============================
Provides a mock REST API endpoint that mimics Property Finder (PF) / Bayut /
Dubai Rest API style property listing portals -- no external dependency,
runs entirely inside Odoo.

Use for integration testing, frontend development, and demo scenarios.

Endpoints (all under /api/v1/property-portal/):
  GET  /properties          → Paginated listing (search, filter, sort)
  GET  /properties/<id>     → Single property detail
  GET  /properties/search   → Unified search (text + filters)
  GET  /locations           → Area / community autocomplete
  GET  /agents              → Agent directory
  GET  /stats               → Aggregate market stats
  POST /inquiry             → Lead / inquiry submission

Response format mirrors common property portal conventions:
  {
    "success": true,
    "data": { ... },
    "pagination": { "page": 1, "per_page": 20, "total": 150 },
    "server_time": "2026-07-11T06:07:18Z"
  }
    """,
    'category': 'Technical/Demo',
    'author': 'SGC',
    'website': 'https://sgc-tech.ai',
    'depends': ['base'],
    'data': [],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'OPL-1',
}
