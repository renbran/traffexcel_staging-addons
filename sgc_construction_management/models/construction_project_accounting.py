# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ConstructionProjectPnl(models.Model):
    """Project-level Profit & Loss summary backed by SQL view v_construction_project_pnl."""
    _name = 'construction.project.pnl'
    _description = 'Construction Project P&L'
    _auto = False
    _order = 'project_id'

    project_id = fields.Many2one('construction.project', string='Project', readonly=True)
    project_name = fields.Char(string='Project Name', readonly=True)
    project_state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)
    analytic_account_name = fields.Char(string='Analytic Account Name', readonly=True)
    contract_value = fields.Monetary(string='Contract Value', currency_field='currency_id', readonly=True)
    currency_id = fields.Many2one(related='project_id.currency_id', string='Currency')
    start_date = fields.Date(readonly=True)
    end_date = fields.Date(readonly=True)

    # Revenue
    total_revenue = fields.Monetary(string='Total Revenue', currency_field='currency_id', readonly=True)
    invoice_count = fields.Integer(string='Invoices', readonly=True)
    revenue_received = fields.Monetary(string='Revenue Received', currency_field='currency_id', readonly=True)

    # COGS
    total_cogs = fields.Monetary(string='Total COGS', currency_field='currency_id', readonly=True)
    bill_count = fields.Integer(string='Vendor Bills', readonly=True)
    bills_paid = fields.Monetary(string='Bills Paid', currency_field='currency_id', readonly=True)

    # Profit
    gross_profit = fields.Monetary(string='Gross Profit', currency_field='currency_id', readonly=True)

    # Payments
    total_payments_received = fields.Monetary(string='Payments Received', currency_field='currency_id', readonly=True)
    outstanding_revenue = fields.Monetary(string='Outstanding Revenue', currency_field='currency_id', readonly=True)
    total_payments_made = fields.Monetary(string='Payments Made', currency_field='currency_id', readonly=True)
    outstanding_payables = fields.Monetary(string='Outstanding Payables', currency_field='currency_id', readonly=True)

    # Progress
    percent_complete = fields.Float(string='% Complete', readonly=True)

    def init(self):
        tools = self.env['tools']
        if tools.table_exists(self.env.cr, 'v_construction_project_pnl'):
            tools.drop_view(self.env.cr, 'v_construction_project_pnl')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW v_construction_project_pnl AS
            WITH revenue AS (
              SELECT
                key::integer as analytic_account_id,
                SUM(aml.credit - aml.debit) as total_revenue,
                COUNT(DISTINCT aml.move_id) as invoice_count
              FROM account_move_line aml
              JOIN LATERAL jsonb_each_text(aml.analytic_distribution) as dist(key, value) ON true
              JOIN account_account aa ON aml.account_id = aa.id
              JOIN account_move am ON aml.move_id = am.id
              WHERE aml.analytic_distribution IS NOT NULL
              AND aml.analytic_distribution != '{}'::jsonb
              AND aa.account_type = 'income'
              AND am.move_type = 'out_invoice'
              AND am.state IN ('posted', 'paid')
              GROUP BY key
            ),
            revenue_paid AS (
              SELECT
                key::integer as analytic_account_id,
                SUM(aml.credit - aml.debit) as revenue_received
              FROM account_move_line aml
              JOIN LATERAL jsonb_each_text(aml.analytic_distribution) as dist(key, value) ON true
              JOIN account_account aa ON aml.account_id = aa.id
              JOIN account_move am ON aml.move_id = am.id
              WHERE aml.analytic_distribution IS NOT NULL
              AND aml.analytic_distribution != '{}'::jsonb
              AND aa.account_type = 'income'
              AND am.move_type = 'out_invoice'
              AND am.state IN ('posted', 'paid')
              AND am.payment_state IN ('paid', 'partial')
              GROUP BY key
            ),
            cogs AS (
              SELECT
                key::integer as analytic_account_id,
                SUM(aml.debit - aml.credit) as total_cogs,
                COUNT(DISTINCT aml.move_id) as bill_count
              FROM account_move_line aml
              JOIN LATERAL jsonb_each_text(aml.analytic_distribution) as dist(key, value) ON true
              JOIN account_account aa ON aml.account_id = aa.id
              JOIN account_move am ON aml.move_id = am.id
              WHERE aml.analytic_distribution IS NOT NULL
              AND aml.analytic_distribution != '{}'::jsonb
              AND aa.account_type = 'expense_direct_cost'
              AND am.move_type = 'in_invoice'
              AND am.state IN ('posted', 'paid')
              GROUP BY key
            ),
            cogs_paid AS (
              SELECT
                key::integer as analytic_account_id,
                SUM(aml.debit - aml.credit) as bills_paid
              FROM account_move_line aml
              JOIN LATERAL jsonb_each_text(aml.analytic_distribution) as dist(key, value) ON true
              JOIN account_account aa ON aml.account_id = aa.id
              JOIN account_move am ON aml.move_id = am.id
              WHERE aml.analytic_distribution IS NOT NULL
              AND aml.analytic_distribution != '{}'::jsonb
              AND aa.account_type = 'expense_direct_cost'
              AND am.move_type = 'in_invoice'
              AND am.state IN ('posted', 'paid')
              AND am.payment_state IN ('paid', 'partial')
              GROUP BY key
            )
            SELECT
              cp.id as id,
              cp.id as project_id,
              cp.name as project_name,
              cp.state as project_state,
              cp.analytic_account_id,
              aaa.name->>'en_US' as analytic_account_name,
              cp.contract_value,
              cp.start_date,
              cp.end_date,
              COALESCE(rev.total_revenue, 0) as total_revenue,
              COALESCE(rev.invoice_count, 0) as invoice_count,
              COALESCE(rp.revenue_received, 0) as revenue_received,
              COALESCE(cogs.total_cogs, 0) as total_cogs,
              COALESCE(cogs.bill_count, 0) as bill_count,
              COALESCE(cp2.bills_paid, 0) as bills_paid,
              COALESCE(rev.total_revenue, 0) - COALESCE(cogs.total_cogs, 0) as gross_profit,
              COALESCE(rp.revenue_received, 0) as total_payments_received,
              COALESCE(rev.total_revenue, 0) - COALESCE(rp.revenue_received, 0) as outstanding_revenue,
              COALESCE(cp2.bills_paid, 0) as total_payments_made,
              COALESCE(cogs.total_cogs, 0) - COALESCE(cp2.bills_paid, 0) as outstanding_payables,
              CASE WHEN cp.contract_value > 0
                THEN ROUND((COALESCE(rev.total_revenue, 0) / cp.contract_value * 100)::numeric, 1)
                ELSE 0
              END as percent_complete
            FROM construction_project cp
            LEFT JOIN account_analytic_account aaa ON cp.analytic_account_id = aaa.id
            LEFT JOIN revenue rev ON cp.analytic_account_id = rev.analytic_account_id
            LEFT JOIN revenue_paid rp ON cp.analytic_account_id = rp.analytic_account_id
            LEFT JOIN cogs ON cp.analytic_account_id = cogs.analytic_account_id
            LEFT JOIN cogs_paid cp2 ON cp.analytic_account_id = cp2.analytic_account_id
            WHERE cp.state = 'active'
            ORDER BY cp.id
        """)


class ConstructionProjectInvoiceLine(models.Model):
    """Invoice/Bill line detail per project backed by SQL view v_construction_project_invoices."""
    _name = 'construction.project.invoice.line'
    _description = 'Construction Project Invoice Line'
    _auto = False
    _order = 'project_id, invoice_date'

    project_id = fields.Many2one('construction.project', string='Project', readonly=True)
    project_name = fields.Char(string='Project Name', readonly=True)
    move_id = fields.Many2one('account.move', string='Invoice/Bill', readonly=True)
    invoice_ref = fields.Char(string='Reference', readonly=True)
    invoice_date = fields.Date(string='Date', readonly=True)
    move_type = fields.Selection([
        ('out_invoice', 'Customer Invoice'),
        ('in_invoice', 'Vendor Bill'),
        ('out_refund', 'Credit Note'),
        ('in_refund', 'Debit Note'),
    ], string='Type', readonly=True)
    move_state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)
    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
        ('partial', 'Partial'),
        ('reversed', 'Reversed'),
        ('invoiced', 'Invoiced'),
    ], string='Payment Status', readonly=True)
    analytic_distribution = fields.Json(string='Analytic Distribution', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', readonly=True)
    account_type = fields.Selection(related='account_id.account_type', string='Account Type')
    account_code = fields.Char(string='Account Code', readonly=True)
    account_name = fields.Char(string='Account', readonly=True)
    account_id = fields.Many2one('account.account', string='Account', readonly=True)
    debit = fields.Monetary(string='Debit', currency_field='currency_id', readonly=True)
    credit = fields.Monetary(string='Credit', currency_field='currency_id', readonly=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', readonly=True)
    currency_id = fields.Many2one(related='project_id.currency_id')
    line_description = fields.Char(string='Description', readonly=True)

    def init(self):
        tools = self.env['tools']
        if tools.table_exists(self.env.cr, 'v_construction_project_invoices'):
            tools.drop_view(self.env.cr, 'v_construction_project_invoices')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW v_construction_project_invoices AS
            SELECT
              ROW_NUMBER() OVER () as id,
              cp.id as project_id,
              cp.name as project_name,
              am.id as move_id,
              am.name as invoice_ref,
              am.invoice_date,
              am.move_type,
              am.state as move_state,
              am.payment_state,
              aml.analytic_distribution,
              key::integer as analytic_account_id,
              aml.account_id,
              aa.account_type,
              (aa.code_store->>'1') as account_code,
              aa.name->>'en_US' as account_name,
              aml.debit,
              aml.credit,
              (aml.credit - aml.debit) as amount,
              aml.name as line_description
            FROM construction_project cp
            JOIN account_move_line aml ON aml.analytic_distribution IS NOT NULL
              AND aml.analytic_distribution != '{}'::jsonb
              AND aml.analytic_distribution ? cp.analytic_account_id::text
            JOIN LATERAL jsonb_each_text(aml.analytic_distribution) as dist(key, value) ON true
            JOIN account_account aa ON aml.account_id = aa.id
            JOIN account_move am ON aml.move_id = am.id
            WHERE cp.state = 'active'
              AND key::integer = cp.analytic_account_id
            ORDER BY cp.id, am.invoice_date, am.name
        """)


class ConstructionProjectAnalyticLine(models.Model):
    """Analytic line detail per project backed by SQL view v_construction_project_analytic_lines."""
    _name = 'construction.project.analytic.line'
    _description = 'Construction Project Analytic Line'
    _auto = False
    _order = 'project_id, date desc'

    project_id = fields.Many2one('construction.project', string='Project', readonly=True)
    project_name = fields.Char(string='Project Name', readonly=True)
    analytic_line_id = fields.Many2one('account.analytic.line', string='Analytic Line', readonly=True)
    date = fields.Date(string='Date', readonly=True)
    description = fields.Char(string='Description', readonly=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', readonly=True)
    currency_id = fields.Many2one(related='project_id.currency_id')
    general_account_id = fields.Many2one('account.account', string='Account', readonly=True)
    account_code = fields.Char(string='Account Code', readonly=True)
    account_name = fields.Char(string='Account Name', readonly=True)
    move_line_id = fields.Many2one('account.move.line', string='Journal Item', readonly=True)
    move_debit = fields.Monetary(string='Move Debit', currency_field='currency_id', readonly=True)
    move_credit = fields.Monetary(string='Move Credit', currency_field='currency_id', readonly=True)
    move_line_name = fields.Char(string='Move Line Description', readonly=True)

    def init(self):
        tools = self.env['tools']
        if tools.table_exists(self.env.cr, 'v_construction_project_analytic_lines'):
            tools.drop_view(self.env.cr, 'v_construction_project_analytic_lines')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW v_construction_project_analytic_lines AS
            SELECT
              aal.id as id,
              cp.id as project_id,
              cp.name as project_name,
              aal.id as analytic_line_id,
              aal.date,
              aal.name as description,
              aal.amount,
              aal.general_account_id,
              (aa.code_store->>'1') as account_code,
              aa.name->>'en_US' as account_name,
              aal.move_line_id,
              aml.debit as move_debit,
              aml.credit as move_credit,
              aml.name as move_line_name
            FROM account_analytic_line aal
            JOIN construction_project cp ON aal.account_id = cp.analytic_account_id
            LEFT JOIN account_account aa ON aal.general_account_id = aa.id
            LEFT JOIN account_move_line aml ON aal.move_line_id = aml.id
            WHERE cp.state = 'active'
            ORDER BY cp.id, aal.date DESC
        """)
