# -*- coding: utf-8 -*-
import logging
from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

# 23 empty mirror projects (ids 117-139) and their empty mirror analytic accounts
# (ids 147-169). These were confirmed to have zero business dependents.
DUPLICATE_PROJECT_IDS = tuple(range(117, 140))
DUPLICATE_ANALYTIC_IDS = tuple(range(147, 170))


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cleanup_duplicates(cr, env)
    recompute_financials(cr, env)


def cleanup_duplicates(cr, env):
    cr.execute(
        "SELECT COUNT(*) FROM construction_project WHERE id IN %s",
        (DUPLICATE_PROJECT_IDS,)
    )
    project_count = cr.fetchone()[0]
    cr.execute(
        "SELECT COUNT(*) FROM account_analytic_account WHERE id IN %s",
        (DUPLICATE_ANALYTIC_IDS,)
    )
    analytic_count = cr.fetchone()[0]

    if project_count == 0 and analytic_count == 0:
        _logger.info("Duplicate cleanup already done; skipping.")
        return

    _logger.info(
        "Cleaning up %s duplicate project(s) and %s duplicate analytic account(s).",
        project_count, analytic_count,
    )

    # Clean up residual FK/tracking data for both models before hard deletes.
    for model, ids in [
        ('construction.project', DUPLICATE_PROJECT_IDS),
        ('account.analytic.account', DUPLICATE_ANALYTIC_IDS),
    ]:
        cr.execute("""
            DELETE FROM mail_tracking_value
            WHERE mail_message_id IN (
                SELECT id FROM mail_message WHERE model = %s AND res_id IN %s
            )
        """, (model, ids))
        cr.execute(
            "DELETE FROM mail_message WHERE model = %s AND res_id IN %s",
            (model, ids)
        )
        cr.execute(
            "DELETE FROM mail_followers WHERE res_model = %s AND res_id IN %s",
            (model, ids)
        )
        cr.execute(
            "DELETE FROM ir_attachment WHERE res_model = %s AND res_id IN %s",
            (model, ids)
        )
        cr.execute(
            "DELETE FROM ir_model_data WHERE model = %s AND res_id IN %s",
            (model, ids)
        )

    # Delete the duplicate projects first (they hold the FK to analytic accounts).
    if project_count:
        cr.execute(
            "DELETE FROM construction_project WHERE id IN %s",
            (DUPLICATE_PROJECT_IDS,)
        )
        _logger.info("Deleted %s duplicate construction.project rows.", project_count)

    # Delete the duplicate analytic accounts.
    if analytic_count:
        cr.execute(
            "DELETE FROM account_analytic_account WHERE id IN %s",
            (DUPLICATE_ANALYTIC_IDS,)
        )
        _logger.info("Deleted %s duplicate account.analytic.account rows.", analytic_count)


def recompute_financials(cr, env):
    Project = env['construction.project']
    projects = Project.search([])
    if not projects:
        _logger.info("No construction.project records found; skipping financial recomputation.")
        return

    _logger.info("Recomputing financial fields for %s project(s).", len(projects))

    # Call the ORM compute directly; store=True fields are only in cache after a
    # bare compute call, so we persist them with SQL afterward.
    projects._compute_financials()

    update_sql = """
        UPDATE construction_project
        SET total_billed = %s,
            total_expenses = %s,
            total_received = %s,
            outstanding_balance = %s,
            profit_margin = %s,
            billing_percent = %s,
            margin_percent = %s,
            receipt_percent = %s,
            expense_vs_billed_percent = %s,
            budget_consumed = %s,
            invoice_count = %s,
            vendor_bill_count = %s
        WHERE id = %s
    """
    for project in projects:
        cr.execute(update_sql, (
            project.total_billed or 0.0,
            project.total_expenses or 0.0,
            project.total_received or 0.0,
            project.outstanding_balance or 0.0,
            project.profit_margin or 0.0,
            project.billing_percent or 0.0,
            project.margin_percent or 0.0,
            project.receipt_percent or 0.0,
            project.expense_vs_billed_percent or 0.0,
            project.budget_consumed or 0.0,
            project.invoice_count or 0,
            project.vendor_bill_count or 0,
            project.id,
        ))

    _logger.info("Financial recomputation completed for %s project(s).", len(projects))
