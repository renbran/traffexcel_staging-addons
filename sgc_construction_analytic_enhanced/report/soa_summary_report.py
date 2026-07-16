# -*- coding: utf-8 -*-
from odoo import api, models, _


class SoASummaryReport(models.AbstractModel):
    _name = "report.sgc_construction_analytic_enhanced.report_soa_summary"
    _description = "SOA Summary Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["construction.project"].browse(docids)

        report_data = {}
        for project in docs:
            if not project.analytic_account_id:
                report_data[project.id] = {
                    "total_revenue": 0.0,
                    "total_expenses": 0.0,
                    "invoice_count": 0,
                    "bill_count": 0,
                }
                continue

            analytic_id_str = str(project.analytic_account_id.id)

            lines = self.env["account.move.line"].search([
                ("parent_state", "=", "posted"),
                ("analytic_distribution", "in", [project.analytic_account_id.id]),
                ("move_id.move_type", "in", ("out_invoice", "out_refund", "in_invoice", "in_refund")),
            ])

            moves = lines.mapped("move_id")
            invoices = moves.filtered(lambda m: m.move_type in ("out_invoice", "out_refund"))
            bills = moves.filtered(lambda m: m.move_type in ("in_invoice", "in_refund"))

            total_revenue = sum(invoices.mapped("amount_total_signed"))
            total_expenses = sum(bills.mapped("amount_total_signed"))

            report_data[project.id] = {
                "total_revenue": total_revenue,
                "total_expenses": -total_expenses,  # flip sign for display
                "invoice_count": len(invoices),
                "bill_count": len(bills),
                "invoices": invoices,
                "bills": bills,
            }

        return {
            "doc_ids": docids,
            "doc_model": "construction.project",
            "docs": docs,
            "report_data": report_data,
        }