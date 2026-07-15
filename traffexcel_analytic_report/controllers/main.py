# -*- coding: utf-8 -*-
import io
from datetime import date

from odoo import http
from odoo.http import request

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


class ProjectStatementController(http.Controller):
    """Download a per-construction-project analytic statement as XLSX.

    One summary sheet (one row per project: income / costs / balance) and
    one detail sheet listing every analytic line grouped by project.
    """

    @http.route('/traffexcel/project_statement/xlsx', type='http', auth='user')
    def project_statement_xlsx(self, date_from=None, date_to=None, **kw):
        env = request.env
        company = env.company

        plan = env['account.analytic.plan'].search(
            [('name', '=', 'Construction Projects')], limit=1)
        if not plan:
            # fall back to any plan so the download still works
            plan = env['account.analytic.plan'].search([], limit=1)

        accounts = env['account.analytic.account'].search(
            [('plan_id', 'child_of', plan.id)], order='name')

        domain = [('auto_account_id', 'in', accounts.ids)]
        if date_from:
            domain.append(('date', '>=', date_from))
        if date_to:
            domain.append(('date', '<=', date_to))
        lines = env['account.analytic.line'].search(domain, order='date')

        by_account = {}
        for line in lines:
            by_account.setdefault(line.auto_account_id.id, []).append(line)

        output = io.BytesIO()
        wb = xlsxwriter.Workbook(output, {'in_memory': True})

        title_fmt = wb.add_format({'bold': True, 'font_size': 14})
        head_fmt = wb.add_format({
            'bold': True, 'bg_color': '#714B67', 'font_color': '#FFFFFF',
            'border': 1})
        money_fmt = wb.add_format({'num_format': '#,##0.00'})
        money_bold = wb.add_format({'num_format': '#,##0.00', 'bold': True,
                                    'top': 1})
        date_fmt = wb.add_format({'num_format': 'yyyy-mm-dd'})
        proj_fmt = wb.add_format({'bold': True, 'bg_color': '#F1EAEF'})
        proj_money = wb.add_format({'bold': True, 'bg_color': '#F1EAEF',
                                    'num_format': '#,##0.00'})

        # ---- Summary sheet -------------------------------------------------
        ws = wb.add_worksheet('Summary')
        ws.set_column(0, 0, 45)
        ws.set_column(1, 3, 18)
        ws.write(0, 0, 'Project Statement - %s' % company.name, title_fmt)
        ws.write(1, 0, 'Plan: %s' % plan.name)
        ws.write(2, 0, 'Period: %s -> %s' % (date_from or 'beginning',
                                             date_to or date.today()))
        row = 4
        for col, label in enumerate(['Project', 'Income', 'Costs', 'Balance']):
            ws.write(row, col, label, head_fmt)
        row += 1
        tot_inc = tot_cost = 0.0
        for account in accounts:
            acc_lines = by_account.get(account.id, [])
            if not acc_lines:
                continue
            income = sum(l.amount for l in acc_lines if l.amount > 0)
            costs = sum(l.amount for l in acc_lines if l.amount < 0)
            tot_inc += income
            tot_cost += costs
            ws.write(row, 0, account.name)
            ws.write_number(row, 1, income, money_fmt)
            ws.write_number(row, 2, costs, money_fmt)
            ws.write_number(row, 3, income + costs, money_fmt)
            row += 1
        ws.write(row, 0, 'Total', money_bold)
        ws.write_number(row, 1, tot_inc, money_bold)
        ws.write_number(row, 2, tot_cost, money_bold)
        ws.write_number(row, 3, tot_inc + tot_cost, money_bold)

        # ---- Details sheet -------------------------------------------------
        ws2 = wb.add_worksheet('Details')
        ws2.set_column(0, 0, 12)
        ws2.set_column(1, 1, 50)
        ws2.set_column(2, 3, 30)
        ws2.set_column(4, 4, 16)
        row = 0
        for col, label in enumerate(
                ['Date', 'Description', 'Partner', 'Financial Account',
                 'Amount']):
            ws2.write(row, col, label, head_fmt)
        row += 1
        for account in accounts:
            acc_lines = by_account.get(account.id, [])
            if not acc_lines:
                continue
            ws2.merge_range(row, 0, row, 3, account.name, proj_fmt)
            ws2.write_number(
                row, 4, sum(l.amount for l in acc_lines), proj_money)
            row += 1
            for line in acc_lines:
                ws2.write_datetime(row, 0, line.date, date_fmt)
                ws2.write(row, 1, line.name or '')
                ws2.write(row, 2, line.partner_id.display_name or '')
                ws2.write(row, 3, line.general_account_id.display_name or '')
                ws2.write_number(row, 4, line.amount, money_fmt)
                row += 1

        wb.close()
        output.seek(0)
        filename = 'project_statement_%s.xlsx' % date.today().isoformat()
        return request.make_response(output.read(), headers=[
            ('Content-Type',
             'application/vnd.openxmlformats-officedocument'
             '.spreadsheetml.sheet'),
            ('Content-Disposition', http.content_disposition(filename)),
        ])
