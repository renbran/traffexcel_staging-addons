# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountPaymentPDC(models.Model):
    _inherit = 'account.payment'

    # ── PDC toggle ──────────────────────────────────────────────────────────
    is_pdc = fields.Boolean(string='Is PDC / BG', default=False, copy=False)

    pdc_type = fields.Selection([
        ('customer_cheque', 'Customer PDC Received'),
        ('vendor_cheque',   'Vendor PDC Issued'),
        ('bank_guarantee',  'Bank Guarantee (BG)'),
        ('performance_bond','Performance Bond'),
    ], string='PDC / BG Type', copy=False)

    pdc_reference = fields.Char(
        string='PDC Reference', copy=False, readonly=True,
        help='Auto-generated reference e.g. PDC/2026/001',
    )

    # ── Instrument details ───────────────────────────────────────────────────
    pdc_cheque_no = fields.Char(string='Cheque / Instrument No.')
    pdc_due_date  = fields.Date(string='Due / Maturity Date')
    pdc_bank_name = fields.Char(string='Issuing Bank')
    pdc_bank_branch = fields.Char(string='Bank Branch')
    pdc_drawer_name = fields.Char(string='Drawer Name',
        help='Name as written on cheque / instrument (if different from partner)')
    pdc_beneficiary = fields.Char(string='Beneficiary Name')

    # ── Bank Guarantee / Bond extras ─────────────────────────────────────────
    pdc_bg_number      = fields.Char(string='BG / Bond Number')
    pdc_bg_expiry_date = fields.Date(string='BG / Bond Expiry Date')
    pdc_bg_issuing_bank = fields.Char(string='BG Issuing Bank')

    # ── Linked construction project ─────────────────────────────────────────
    pdc_project_id = fields.Many2one(
        'construction.project', string='Construction Project',
        index=True, copy=False,
    )

    # ── Workflow state ───────────────────────────────────────────────────────
    pdc_status = fields.Selection([
        ('draft',      'Draft'),
        ('received',   'Received / Issued'),
        ('deposited',  'Deposited to Bank'),
        ('cleared',    'Cleared'),
        ('bounced',    'Bounced / Returned'),
    ], string='PDC Status', default='draft', copy=False, tracking=True)

    pdc_deposit_date  = fields.Date(string='Deposited Date', copy=False)
    pdc_clearing_date = fields.Date(string='Cleared Date', copy=False)
    pdc_bounce_date   = fields.Date(string='Bounce Date', copy=False)
    pdc_bounce_reason = fields.Char(string='Bounce Reason', copy=False)
    pdc_notes = fields.Text(string='Notes / Remarks')

    # ── Computed display helpers ─────────────────────────────────────────────
    pdc_days_to_due = fields.Integer(
        string='Days to Due', compute='_compute_pdc_days_to_due', store=False,
    )
    pdc_is_overdue = fields.Boolean(
        string='Overdue', compute='_compute_pdc_days_to_due', store=False,
    )

    @api.depends('pdc_due_date', 'pdc_status')
    def _compute_pdc_days_to_due(self):
        today = fields.Date.today()
        for rec in self:
            if rec.pdc_due_date and rec.pdc_status not in ('cleared', 'bounced'):
                delta = (rec.pdc_due_date - today).days
                rec.pdc_days_to_due = delta
                rec.pdc_is_overdue = delta < 0
            else:
                rec.pdc_days_to_due = 0
                rec.pdc_is_overdue = False

    # ── Sequence assignment ──────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('is_pdc') and not vals.get('pdc_reference'):
                vals['pdc_reference'] = self.env['ir.sequence'].next_by_code('sgc.pdc.reference') or '/'
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            if vals.get('is_pdc') and not rec.pdc_reference:
                vals['pdc_reference'] = self.env['ir.sequence'].next_by_code('sgc.pdc.reference') or '/'
                break
        return super().write(vals)

    # ── Workflow actions ─────────────────────────────────────────────────────
    def action_pdc_receive(self):
        for rec in self:
            rec._pdc_check_required()
            if rec.pdc_status != 'draft':
                raise UserError(_('Only Draft PDC can be marked as Received/Issued.'))
            rec.pdc_status = 'received'

    def action_pdc_deposit(self):
        for rec in self:
            if rec.pdc_status != 'received':
                raise UserError(_('Only Received/Issued PDC can be deposited.'))
            rec.pdc_deposit_date = fields.Date.today()
            rec.pdc_status = 'deposited'

    def action_pdc_clear(self):
        for rec in self:
            if rec.pdc_status != 'deposited':
                raise UserError(_('Only Deposited PDC can be marked as Cleared.'))
            rec.pdc_clearing_date = fields.Date.today()
            rec.pdc_status = 'cleared'
            # Post the actual Odoo payment if still in draft
            if rec.state == 'draft':
                rec.action_post()

    def action_pdc_bounce(self):
        return {
            'name': _('Record Bounce / Return'),
            'type': 'ir.actions.act_window',
            'res_model': 'sgc.pdc.bounce.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_payment_id': self.id},
        }

    def _pdc_check_required(self):
        for rec in self:
            missing = []
            if not rec.pdc_cheque_no:
                missing.append(_('Cheque / Instrument No.'))
            if not rec.pdc_due_date:
                missing.append(_('Due / Maturity Date'))
            if not rec.pdc_bank_name:
                missing.append(_('Issuing Bank'))
            if missing:
                raise UserError(
                    _('Please fill in the following PDC fields before proceeding:\n• %s')
                    % '\n• '.join(missing)
                )

    # ── Print action ─────────────────────────────────────────────────────────
    def action_print_pdc_slip(self):
        return self.env.ref('sgc_pdc_management.action_report_pdc_slip').report_action(self)

    def action_print_pdc_register(self):
        return self.env.ref('sgc_pdc_management.action_report_pdc_register').report_action(self)


class SgcPdcBounceWizard(models.TransientModel):
    _name = 'sgc.pdc.bounce.wizard'
    _description = 'PDC Bounce / Return Wizard'

    payment_id   = fields.Many2one('account.payment', required=True)
    bounce_date   = fields.Date(required=True, default=fields.Date.today)
    bounce_reason = fields.Char(string='Reason', required=True)

    def action_confirm_bounce(self):
        rec = self.payment_id
        if rec.pdc_status != 'deposited':
            raise UserError(_('PDC must be in Deposited state to record a bounce.'))
        rec.pdc_bounce_date   = self.bounce_date
        rec.pdc_bounce_reason = self.bounce_reason
        rec.pdc_status        = 'bounced'
        return {'type': 'ir.actions.act_window_close'}
