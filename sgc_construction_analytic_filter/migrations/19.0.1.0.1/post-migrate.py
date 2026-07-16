# -*- coding: utf-8 -*-
"""Post-migration: recompute construction_project_id on existing account.move records.

Runs once when the module is upgraded to 19.0.1.0.1 or later. Ensures the
stored computed field is populated for invoices that already had analytic
distributions before the field existed in the DB.
"""
import logging

from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not version:
        return
    _logger.info(
        "Recomputing construction_project_id on existing account.move records "
        "(post-migrate to %s)...",
        version,
    )
    env = api.Environment(cr, SUPERUSER_ID, {})
    moves = env["account.move"].search([
        ("move_type", "in", ("out_invoice", "in_invoice", "out_refund", "in_refund")),
    ])
    _logger.info("Found %d moves to recompute", len(moves))
    if moves:
        moves.invalidate_recordset(["construction_project_id"])
        moves._compute_construction_project_id()
    _logger.info("construction_project_id recompute complete.")