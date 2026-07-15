# -*- coding: utf-8 -*-
import io
import xlsxwriter
from odoo import models, fields, api

class ProjectWIPXlsx(models.AbstractModel):
    _name = 'report.sgc_construction_management.report_wip_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'WIP Report Excel'

    def generate_xlsx_report(self, workbook, data, projects):
        sheet = workbook.add_worksheet('WIP Report')

        # Formats
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        money = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        percent = workbook.add_format({'num_format': '0.00%', 'border': 1})
        header = workbook.add_format({'bold': True, 'size': 14, 'align': 'center'})
        border = workbook.add_format({'border': 1})

        sheet.merge_range('A1:G1', 'WORK IN PROGRESS (WIP) REPORT', header)

        # Headers
        headers = ['Project Name', 'Contract Value', 'Progress %', 'Earned Revenue', 'Total Billed', 'Over/(Under) Billing', 'Expenses']
        for col, title in enumerate(headers):
            sheet.write(2, col, title, bold)

        row = 3
        for project in projects:
            earned = (project.contract_value or 0) * ((project.progress or 0) / 100)
            over_under = earned - (project.total_billed or 0)

            sheet.write(row, 0, project.name, border)
            sheet.write(row, 1, project.contract_value or 0, money)
            sheet.write(row, 2, (project.progress or 0) / 100, percent)
            sheet.write(row, 3, earned, money)
            sheet.write(row, 4, project.total_billed or 0, money)
            sheet.write(row, 5, over_under, money)
            sheet.write(row, 6, project.total_expenses or 0, money)
            row += 1

        sheet.set_column('A:A', 30)
        sheet.set_column('B:G', 15)

class RABillingXlsx(models.AbstractModel):
    _name = 'report.sgc_construction_management.report_ra_billing_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'RA Billing Excel'

    def generate_xlsx_report(self, workbook, data, billings):
        sheet = workbook.add_worksheet('RA Billing')
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        money = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        border = workbook.add_format({'border': 1})

        sheet.write(0, 0, 'RA Billing Report', bold)

        headers = ['Item Description', 'Unit', 'BOQ Qty', 'Rate', 'Prev. Qty', 'Curr. Qty', 'Cum. Qty', 'Amount']
        for col, title in enumerate(headers):
            sheet.write(2, col, title, bold)

        row = 3
        for billing in billings:
            for line in billing.line_ids:
                sheet.write(row, 0, line.boq_line_description, border)
                sheet.write(row, 1, line.uom_id.name if line.uom_id else '', border)
                sheet.write(row, 2, line.boq_qty, border)
                sheet.write(row, 3, line.unit_rate, money)
                sheet.write(row, 4, line.qty_previous, border)
                sheet.write(row, 5, line.qty_current, border)
                sheet.write(row, 6, line.qty_cumulative, border)
                sheet.write(row, 7, line.amount, money)
                row += 1

        sheet.set_column('A:A', 40)
        sheet.set_column('B:H', 12)

class ProjectProfitabilityXlsx(models.AbstractModel):
    _name = 'report.sgc_construction_management.report_profitability_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Profitability Excel'

    def generate_xlsx_report(self, workbook, data, projects):
        sheet = workbook.add_worksheet('Profitability')
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        money = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        percent = workbook.add_format({'num_format': '0.00%', 'border': 1})
        border = workbook.add_format({'border': 1})

        sheet.write(0, 0, 'Project Profitability Report', bold)

        headers = ['Project Name', 'Contract Value', 'Total Billed', 'Direct Costs', 'Gross Margin', 'Margin %']
        for col, title in enumerate(headers):
            sheet.write(2, col, title, bold)

        row = 3
        for project in projects:
            margin = (project.total_billed or 0) - (project.total_expenses or 0)
            sheet.write(row, 0, project.name, border)
            sheet.write(row, 1, project.contract_value or 0, money)
            sheet.write(row, 2, project.total_billed or 0, money)
            sheet.write(row, 3, project.total_expenses or 0, money)
            sheet.write(row, 4, margin, money)
            sheet.write(row, 5, (project.margin_percent or 0) / 100, percent)
            row += 1

        sheet.set_column('A:A', 30)
        sheet.set_column('B:F', 15)


class ProjectSoAXlsx(models.AbstractModel):
    _name = 'report.sgc_construction_management.report_project_soa_xlsx'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Project Statement of Account Excel'

    def generate_xlsx_report(self, workbook, data, projects):
        bold = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
        money = workbook.add_format({'num_format': '#,##0.00', 'border': 1})
        date_fmt = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1})
        border = workbook.add_format({'border': 1})
        title_fmt = workbook.add_format({'bold': True, 'size': 14, 'align': 'center'})
        section_fmt = workbook.add_format({'bold': True, 'bg_color': '#EFEFEF', 'border': 1})

        for project in projects:
            sheet = workbook.add_worksheet((project.name or 'Project')[:31])
            sheet.merge_range('A1:G1', 'PROJECT STATEMENT OF ACCOUNT', title_fmt)
            sheet.write('A2', 'Project:', bold)
            sheet.write('B2', project.name or '', border)
            sheet.write('A3', 'Analytic Account:', bold)
            sheet.write('B3', project.analytic_account_id.display_name or '', border)

            if not project.analytic_account_id:
                sheet.write('A5', 'No analytic account linked to this project.', bold)
                continue

            lines = self.env['account.move.line'].search([
                ('parent_state', '=', 'posted'),
                ('analytic_distribution', 'in', [project.analytic_account_id.id]),
                ('move_id.move_type', 'in', ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')),
            ])
            moves = lines.mapped('move_id')
            invoices = moves.filtered(lambda m: m.move_type in ('out_invoice', 'out_refund')).sorted('invoice_date')
            bills = moves.filtered(lambda m: m.move_type in ('in_invoice', 'in_refund')).sorted('invoice_date')

            headers = ['Date', 'Number', 'Partner', 'Reference', 'Type', 'Total', 'Currency']
            type_sel = {'out_invoice': 'Customer Invoice', 'out_refund': 'Customer Credit Note',
                        'in_invoice': 'Vendor Bill', 'in_refund': 'Vendor Credit Note'}

            row = 5
            sheet.merge_range(row, 0, row, 6, 'INVOICES (AR)', section_fmt)
            row += 1
            for col, h in enumerate(headers):
                sheet.write(row, col, h, bold)
            row += 1
            inv_total = 0.0
            for inv in invoices:
                sheet.write(row, 0, inv.invoice_date or '', date_fmt)
                sheet.write(row, 1, inv.name or '', border)
                sheet.write(row, 2, inv.partner_id.display_name or '', border)
                sheet.write(row, 3, inv.ref or '', border)
                sheet.write(row, 4, type_sel.get(inv.move_type, inv.move_type), border)
                sheet.write(row, 5, inv.amount_total_signed or 0.0, money)
                sheet.write(row, 6, inv.currency_id.name or '', border)
                inv_total += inv.amount_total_signed or 0.0
                row += 1
            sheet.write(row, 0, 'Invoices Total', bold)
            sheet.write(row, 5, inv_total, money)
            row += 2

            sheet.merge_range(row, 0, row, 6, 'BILLS (AP)', section_fmt)
            row += 1
            for col, h in enumerate(headers):
                sheet.write(row, col, h, bold)
            row += 1
            bill_total = 0.0
            for bill in bills:
                ap_amount = -(bill.amount_total_signed or 0.0)
                sheet.write(row, 0, bill.invoice_date or '', date_fmt)
                sheet.write(row, 1, bill.name or '', border)
                sheet.write(row, 2, bill.partner_id.display_name or '', border)
                sheet.write(row, 3, bill.ref or '', border)
                sheet.write(row, 4, type_sel.get(bill.move_type, bill.move_type), border)
                sheet.write(row, 5, ap_amount, money)
                sheet.write(row, 6, bill.currency_id.name or '', border)
                bill_total += ap_amount
                row += 1
            sheet.write(row, 0, 'Bills Total', bold)
            sheet.write(row, 5, bill_total, money)
            row += 2

            sheet.write(row, 0, 'Net (AR - AP)', bold)
            sheet.write(row, 5, inv_total - bill_total, money)

            sheet.set_column('A:A', 12)
            sheet.set_column('B:B', 18)
            sheet.set_column('C:C', 30)
            sheet.set_column('D:D', 18)
            sheet.set_column('E:E', 14)
            sheet.set_column('F:F', 16)
            sheet.set_column('G:G', 10)
