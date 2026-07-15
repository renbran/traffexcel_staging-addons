# -*- coding: utf-8 -*-
import io
from datetime import date

from odoo import http
from odoo.http import request

try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None


# Column layout for the Summary sheet. Indexes line up with the list below.
# 0 = Project name, then triplets (Excl / VAT / Incl) for Income, Costs, Balance.
SUMMARY_HEADERS = [
    'Project',
    'Income (excl. VAT)', 'Income VAT', 'Income (incl. VAT)',
    'Costs (excl. VAT)', 'Costs VAT', 'Costs (incl. VAT)',
    'Balance (excl. VAT)', 'Balance VAT', 'Balance (incl. VAT)',
]


class ProjectStatementController(http.Controller):
    """Download a per-construction-project analytic statement as XLSX.

    One summary sheet (one row per project: income / costs / balance) and
    one detail sheet listing every analytic line grouped by project.

    Query parameters
    ----------------
    date_from, date_to : optional date strings (YYYY-MM-DD)
    vat_mode    : 'excl' / 'incl' / 'both' (default 'both')
    entry_state : 'all' / 'posted' / 'draft' (default 'all')

    For each analytic line we look up the source ``account.move.line``
    via ``move_line_id`` (a Many2one already present on
    ``account.analytic.line`` in Odoo 19) and read ``price_total`` minus
    ``price_subtotal`` for the VAT portion. Manual lines (no source move
    line) are treated as zero-rated (VAT = 0; incl. = excl.).
    """

    @http.route('/traffexcel/project_statement/xlsx', type='http', auth='user')
    def project_statement_xlsx(self, date_from=None, date_to=None,
                               vat_mode='both', entry_state='all', **kw):
        env = request.env
        company = env.company

        if vat_mode not in ('excl', 'incl', 'both'):
            vat_mode = 'both'
        if entry_state not in ('all', 'posted', 'draft'):
            entry_state = 'all'

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
        if entry_state != 'all':
            # Lines without a move_line_id are auto-excluded here; this
            # is documented in the wizard's entry_state help text.
            domain.append(('move_line_id.move_id.state', '=', entry_state))
        lines = env['account.analytic.line'].search(domain, order='date')

        # Map source move line -> (price_subtotal, price_total), the
        # stored computed values. price_total - price_subtotal is the
        # VAT portion; no need to re-run tax.compute_all.
        move_lines = lines.mapped('move_line_id').sudo()
        move_line_totals = {}
        for ml in move_lines:
            subtotal = ml.price_subtotal or 0.0
            total = ml.price_total or 0.0
            move_line_totals[ml.id] = (subtotal, total)

        # Each entry: (excl_vat_amount, vat_amount, incl_vat_amount).
        # All values keep the sign of the analytic amount so income
        # (positive) and costs (negative) sum correctly.
        amounts_by_account = {}
        for line in lines:
            excl = line.amount or 0.0
            vat = 0.0
            ml = line.move_line_id
            if ml:
                src_subtotal, src_total = move_line_totals.get(
                    ml.id, (0.0, 0.0))
                src_vat = (src_total or 0.0) - (src_subtotal or 0.0)
                # Scale VAT by the analytic-line / source-line ratio
                # so partial analytic distributions stay proportional.
                if src_subtotal:
                    ratio = excl / src_subtotal
                    vat = src_vat * ratio
                else:
                    vat = src_vat
            incl = excl + vat

            bucket = amounts_by_account.setdefault(line.auto_account_id.id, {
                'excl': 0.0,
                'vat': 0.0,
                'incl': 0.0,
                'lines': [],
            })
            bucket['excl'] += excl
            bucket['vat'] += vat
            bucket['incl'] += incl
            bucket['lines'].append((line, excl, vat, incl))

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
        ws.set_column(1, 9, 18)
        ws.write(0, 0, 'Project Statement - %s' % company.name, title_fmt)
        ws.write(1, 0, 'Plan: %s' % plan.name)
        ws.write(2, 0, 'Period: %s -> %s' % (date_from or 'beginning',
                                             date_to or date.today()))
        ws.write(3, 0, 'Entries: %s   VAT: %s' % (entry_state, vat_mode))
        row = 5
        for col, label in enumerate(SUMMARY_HEADERS):
            ws.write(row, col, label, head_fmt)
        row += 1

        # Hide VAT/Incl columns when the user filtered to a single mode.
        if vat_mode == 'excl':
            for c in (2, 5, 8):
                ws.set_column(c, c, 18, {'hidden': 1})
        elif vat_mode == 'incl':
            for c in (1, 4, 7):
                ws.set_column(c, c, 18, {'hidden': 1})
        # 'both' shows all 9 columns.

        tot_inc_excl = tot_inc_vat = tot_inc_incl = 0.0
        tot_cost_excl = tot_cost_vat = tot_cost_incl = 0.0
        for account in accounts:
            bucket = amounts_by_account.get(account.id)
            if not bucket or not bucket['lines']:
                continue
            inc_excl = inc_vat = inc_incl = 0.0
            cost_excl = cost_vat = cost_incl = 0.0
            for _line, excl, vat, incl in bucket['lines']:
                if excl >= 0:
                    inc_excl += excl
                    inc_vat += vat
                    inc_incl += incl
                else:
                    cost_excl += excl  # negative
                    cost_vat += vat    # negative or zero
                    cost_incl += incl
            tot_inc_excl += inc_excl
            tot_inc_vat += inc_vat
            tot_inc_incl += inc_incl
            tot_cost_excl += cost_excl
            tot_cost_vat += cost_vat
            tot_cost_incl += cost_incl

            ws.write(row, 0, account.name)
            ws.write_number(row, 1, inc_excl, money_fmt)
            ws.write_number(row, 2, inc_vat, money_fmt)
            ws.write_number(row, 3, inc_incl, money_fmt)
            ws.write_number(row, 4, cost_excl, money_fmt)
            ws.write_number(row, 5, cost_vat, money_fmt)
            ws.write_number(row, 6, cost_incl, money_fmt)
            ws.write_number(row, 7, inc_excl + cost_excl, money_fmt)
            ws.write_number(row, 8, inc_vat + cost_vat, money_fmt)
            ws.write_number(row, 9, inc_incl + cost_incl, money_fmt)
            row += 1

        ws.write(row, 0, 'Total', money_bold)
        for col, val in enumerate(
                [tot_inc_excl, tot_inc_vat, tot_inc_incl,
                 tot_cost_excl, tot_cost_vat, tot_cost_incl,
                 tot_inc_excl + tot_cost_excl,
                 tot_inc_vat + tot_cost_vat,
                 tot_inc_incl + tot_cost_incl], start=1):
            ws.write_number(row, col, val, money_bold)
        row += 1

        # ---- Details sheet -------------------------------------------------
        ws2 = wb.add_worksheet('Details')
        ws2.set_column(0, 0, 12)
        ws2.set_column(1, 1, 50)
        ws2.set_column(2, 3, 30)
        ws2.set_column(4, 6, 16)
        row = 0
        detail_headers = [
            'Date', 'Description', 'Partner', 'Financial Account',
            'Amount (excl. VAT)', 'VAT', 'Amount (incl. VAT)',
        ]
        for col, label in enumerate(detail_headers):
            ws2.write(row, col, label, head_fmt)
        row += 1

        # Hide VAT/Incl columns on the details sheet to mirror the summary.
        if vat_mode == 'excl':
            ws2.set_column(5, 6, 16, {'hidden': 1})
        elif vat_mode == 'incl':
            ws2.set_column(4, 5, 16, {'hidden': 1})
            ws2.set_column(6, 6, 16, {'hidden': 1})

        for account in accounts:
            bucket = amounts_by_account.get(account.id)
            if not bucket or not bucket['lines']:
                continue
            ws2.merge_range(row, 0, row, 3, account.name, proj_fmt)
            ws2.write_number(row, 4, bucket['excl'], proj_money)
            ws2.write_number(row, 5, bucket['vat'], proj_money)
            ws2.write_number(row, 6, bucket['incl'], proj_money)
            row += 1
            for line, excl, vat, incl in bucket['lines']:
                ws2.write_datetime(row, 0, line.date, date_fmt)
                ws2.write(row, 1, line.name or '')
                ws2.write(row, 2, line.partner_id.display_name or '')
                ws2.write(row, 3, line.general_account_id.display_name or '')
                ws2.write_number(row, 4, excl, money_fmt)
                ws2.write_number(row, 5, vat, money_fmt)
                ws2.write_number(row, 6, incl, money_fmt)
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
