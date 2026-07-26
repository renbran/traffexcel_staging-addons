# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('construction.project', index=True, string='Construction Project')

    def write(self, vals):
        # An invoice generated from an RA Billing must stay identical to it:
        # its lines can only be changed through the billing (which re-syncs
        # the draft invoice), never edited directly.
        if 'invoice_line_ids' in vals and not self.env.context.get('ra_billing_sync'):
            for move in self:
                if move.state != 'draft' or move.move_type != 'out_invoice':
                    continue
                billing = self.env['construction.ra.billing'].sudo().search(
                    [('move_id', '=', move.id)], limit=1)
                if billing:
                    raise UserError(
                        "Invoice %s is managed by RA Billing %s. "
                        "Edit the RA Billing instead - the invoice is updated automatically." %
                        (move.name or move.ref or move.id, billing.ref)
                    )
        return super().write(vals)

    def _get_distributed_analytic_account_ids(self):
        analytic_ids = set()
        for line in self.line_ids:
            for key in (line.analytic_distribution or {}):
                try:
                    analytic_ids.add(int(key))
                except (TypeError, ValueError):
                    continue
        return analytic_ids

    def _trigger_project_financials_recompute(self):
        # construction.project._compute_financials only depends on analytic_account_id,
        # so it never auto-recomputes when invoices/bills are posted, drafted, or
        # cancelled. Push the recompute explicitly on those lifecycle transitions.
        #
        # Because the dependency (analytic_account_id) doesn't actually change
        # during invoice/bill lifecycle events, the ORM won't persist the
        # recomputed values to the DB even though they are store=True. We must
        # invalidate, recompute, then explicitly UPDATE each row — the same
        # pattern used in hooks._recompute_project_financials().
        analytic_ids = self._get_distributed_analytic_account_ids()
        if not analytic_ids:
            return
        projects = self.env['construction.project'].search([('analytic_account_id', 'in', list(analytic_ids))])
        if not projects:
            return
        for p in projects:
            p.invalidate_recordset()
            p._compute_financials()
            self.env.cr.execute(
                "UPDATE construction_project SET "
                "total_billed=%s, total_expenses=%s, total_received=%s, "
                "outstanding_balance=%s, profit_margin=%s, "
                "billing_percent=%s, margin_percent=%s, receipt_percent=%s, "
                "expense_vs_billed_percent=%s, budget_consumed=%s, "
                "invoice_count=%s, vendor_bill_count=%s "
                "WHERE id=%s",
                (p.total_billed, p.total_expenses, p.total_received,
                 p.outstanding_balance, p.profit_margin,
                 p.billing_percent, p.margin_percent, p.receipt_percent,
                 p.expense_vs_billed_percent, p.budget_consumed,
                 p.invoice_count, p.vendor_bill_count, p.id),
            )

    def _post(self, soft=True):
        posted = super()._post(soft=soft)
        posted._trigger_project_financials_recompute()
        return posted

    def button_draft(self):
        res = super().button_draft()
        self._trigger_project_financials_recompute()
        return res

    def button_cancel(self):
        res = super().button_cancel()
        self._trigger_project_financials_recompute()
        return res
