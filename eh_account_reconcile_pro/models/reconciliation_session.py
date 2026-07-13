# -*- encoding: utf-8 -*-
##############################################################################
#
# ERP Heritage
# Copyright (C) 2026 (https://www.erpheritage.com.au/)
#
##############################################################################
"""
eh.reconciliation.session: tracks an in progress reconciliation context
per user and journal.

A session is opened when a user enters the reconciliation workspace for
a journal. As they match, write off, or skip statement lines, decisions
flow through the session's apply_match and apply_write_off methods. Each
decision creates an eh.reconciliation.audit row and bumps a counter on
the session.

Sessions close manually (button) or implicitly when the user opens the
workspace for a different journal. Closed sessions persist as historical
work logs: how long it took to clear a journal's backlog, how many of
the matches came from the suggestion engine versus manual review.
"""

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import SQL


_ALLOWED_COUNTERS = frozenset({
    'matches_made', 'matches_via_suggestion', 'matches_manual',
    'write_offs', 'skips',
})


class EhReconciliationSession(models.Model):
    _name = 'eh.reconciliation.session'
    _description = "Bank reconciliation session"
    _order = 'opened_at desc'
    _rec_name = 'name'

    name = fields.Char(compute='_compute_name', store=True)

    user_id = fields.Many2one(
        'res.users',
        required=True,
        default=lambda self: self.env.user,
        index=True,
    )
    journal_id = fields.Many2one(
        'account.journal',
        required=True,
        ondelete='cascade',
        index=True,
        domain="[('type', 'in', ('bank', 'cash'))]",
    )
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company,
        index=True,
    )

    opened_at = fields.Datetime(
        required=True,
        default=fields.Datetime.now,
        index=True,
    )
    closed_at = fields.Datetime()
    state = fields.Selection(
        [
            ('open', "Open"),
            ('closed', "Closed"),
        ],
        required=True,
        default='open',
        index=True,
    )

    statements_processed = fields.Integer(default=0)
    matches_made = fields.Integer(default=0)
    matches_via_suggestion = fields.Integer(default=0)
    matches_manual = fields.Integer(default=0)
    write_offs = fields.Integer(default=0)
    skips = fields.Integer(default=0)

    duration_seconds = fields.Integer(
        compute='_compute_duration', store=True,
    )

    audit_ids = fields.One2many(
        'eh.reconciliation.audit', 'session_id',
    )
    audit_count = fields.Integer(compute='_compute_audit_count')

    @api.depends('user_id', 'journal_id', 'opened_at')
    def _compute_name(self):
        for rec in self:
            if rec.opened_at and rec.journal_id:
                ts = fields.Datetime.to_string(rec.opened_at)
                rec.name = "%s %s" % (rec.journal_id.code or '', ts)
            else:
                rec.name = "New Session"

    @api.depends('opened_at', 'closed_at')
    def _compute_duration(self):
        for rec in self:
            if rec.closed_at and rec.opened_at:
                rec.duration_seconds = int(
                    (rec.closed_at - rec.opened_at).total_seconds()
                )
            else:
                rec.duration_seconds = 0

    @api.depends('audit_ids')
    def _compute_audit_count(self):
        for rec in self:
            rec.audit_count = len(rec.audit_ids)

    # ---- onchange (live form feedback) ----

    @api.onchange('journal_id')
    def _onchange_journal_id_company(self):
        """Pin company to the journal's company.

        A journal is single-company in Odoo; if the user picks a journal
        owned by a different company than the session header, the form
        should reconcile that immediately rather than wait for the
        post-save validation to bounce.
        """
        for rec in self:
            if rec.journal_id and rec.journal_id.company_id:
                rec.company_id = rec.journal_id.company_id

    # ---- lifecycle ----

    @api.model
    def open_or_create(self, journal_id):
        """Return the active open session for the current user and journal,
        or create one. Multiple users can have concurrent sessions on the
        same journal; the index is per user.
        """
        existing = self.search(
            [
                ('user_id', '=', self.env.user.id),
                ('journal_id', '=', journal_id),
                ('state', '=', 'open'),
            ],
            limit=1,
        )
        if existing:
            return existing
        return self.create({'journal_id': journal_id})

    def action_close(self):
        """Mark the session closed and stamp closed_at."""
        for rec in self:
            if rec.state == 'closed':
                continue
            rec.write({
                'state': 'closed',
                'closed_at': fields.Datetime.now(),
            })
        return True

    def action_view_audits(self):
        """Open the audit list filtered to this session."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _("Reconciliation Decisions"),
            'res_model': 'eh.reconciliation.audit',
            'view_mode': 'list,form',
            'views': [(False, 'list'), (False, 'form')],
            'domain': [('session_id', '=', self.id)],
            'context': {'default_session_id': self.id},
        }

    # ---- decisions ----

    def apply_match(self, statement_line_id, aml_ids, source='manual'):
        """Reconcile a statement line with the given AML lines.

        :param statement_line_id: id of an account.bank.statement.line.
        :param aml_ids: list of account.move.line ids to reconcile against.
        :param source: 'manual' for an explicit single click,
            'drag_drop' for a drag-and-drop match (counts as manual),
            'suggestion' when the user accepted an engine recommendation,
            'rule' for an account.reconcile.model match,
            'bulk' for a batched apply of several AMLs in one call.
        :return: True on success.
        """
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_("Cannot apply matches on a closed session."))
        if not aml_ids:
            raise UserError(_("apply_match requires at least one aml id."))

        statement_line = self.env['account.bank.statement.line'].browse(
            statement_line_id,
        )
        if not statement_line.exists():
            raise UserError(_("Unknown statement line: %s") % statement_line_id)

        # A statement line that is already fully reconciled must not be
        # re-matched. Without this guard a duplicate apply_match would
        # write an audit row, hit Odoo's reconciliation no-op path, and
        # leave the audit log claiming a match that did not happen on
        # this transaction. Refuse early so the caller surfaces the real
        # state to the user.
        if getattr(statement_line, 'is_reconciled', False):
            raise UserError(_(
                "Statement line %s is already reconciled. Unreconcile it "
                "from the bank statement before matching it again."
            ) % (statement_line.payment_ref or statement_line.id))

        aml_records = self.env['account.move.line'].browse(aml_ids).exists()
        if not aml_records:
            raise UserError(_("No valid AMLs in: %s") % aml_ids)

        # Each candidate AML must still be open (amount_residual non zero
        # and not flagged reconciled). A fully-reconciled AML cannot
        # absorb more reconciliation; Odoo's reconcile() would silently
        # skip it, but the audit row would still record a match. Reject
        # the call instead so the caller gets a clear error.
        already_reconciled = aml_records.filtered(lambda l: l.reconciled)
        if already_reconciled:
            raise UserError(_(
                "These journal items are already reconciled and cannot be "
                "matched again: %s"
            ) % ', '.join(
                a.move_id.name or str(a.id) for a in already_reconciled
            ))

        engine = self.env['eh.reconciliation.suggestion.engine']
        primary = aml_records[0]
        score = engine.score_match(statement_line, primary)
        confidence = score['total']
        rules = ','.join(score['rules_fired'])

        self._perform_reconciliation(statement_line, aml_records)

        Audit = self.env['eh.reconciliation.audit']
        for aml in aml_records:
            Audit.create({
                'session_id': self.id,
                'statement_line_id': statement_line.id,
                'aml_id': aml.id,
                'user_id': self.env.user.id,
                'confidence': confidence,
                'rules_fired': rules,
                'decision': 'match',
                'source': source,
            })

        self._increment_counters('matches_made')
        if source == 'suggestion':
            self._increment_counters('matches_via_suggestion')
        elif source in ('manual', 'drag_drop'):
            # A drag-and-drop match is an explicit manual user action. It
            # carries its own audit source for analytics but still counts
            # as a manual match on the session summary counters.
            self._increment_counters('matches_manual')
        return True

    def apply_write_off(self, statement_line_id, account_id, label=None):
        """Reconcile a statement line as a write off to the given account.

        Creates an audit row with decision=write_off and aml_id null.
        The actual journal entry is posted via the standard Odoo
        write off mechanism in _perform_write_off.
        """
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_("Cannot write off on a closed session."))

        statement_line = self.env['account.bank.statement.line'].browse(
            statement_line_id,
        )
        account = self.env['account.account'].browse(account_id)
        if not statement_line.exists() or not account.exists():
            raise UserError(_("Unknown statement line or account."))

        # Already-reconciled lines cannot be written off again; the
        # write-off would silently no-op while the audit row claimed a
        # decision had been recorded.
        if getattr(statement_line, 'is_reconciled', False):
            raise UserError(_(
                "Statement line %s is already reconciled and cannot be "
                "written off again."
            ) % (statement_line.payment_ref or statement_line.id))

        self._perform_write_off(statement_line, account, label)

        self.env['eh.reconciliation.audit'].create({
            'session_id': self.id,
            'statement_line_id': statement_line.id,
            'aml_id': False,
            'user_id': self.env.user.id,
            'confidence': 0.0,
            'rules_fired': '',
            'decision': 'write_off',
            'source': 'manual',
        })
        self._increment_counters('write_offs')
        return True

    def apply_fx_writeoff(self, statement_line_id, label=None,
                          max_amount=None):
        """Write off the residual of a statement line to the company's
        configured currency-exchange gain or loss account.

        Picks the gain account when residual > 0 (more cash than book),
        the loss account when residual < 0. Refuses when no FX accounts
        are configured on the company so the bank charge does not get
        misrouted to a generic suspense account.

        max_amount: optional safety cap. When set, the absolute residual
        must not exceed this value or the call raises UserError. Lets
        site administrators expose the action behind a "small variance
        only" guardrail (typical: 5.00 of company currency).
        """
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_("Cannot write off on a closed session."))
        statement_line = self.env['account.bank.statement.line'].browse(
            statement_line_id,
        )
        if not statement_line.exists():
            raise UserError(_("Unknown statement line: %s") % statement_line_id)
        if getattr(statement_line, 'is_reconciled', False):
            raise UserError(_(
                "Statement line %s is already reconciled.",
                statement_line.payment_ref or statement_line.id,
            ))
        company = statement_line.company_id or self.env.company
        gain = company.income_currency_exchange_account_id
        loss = company.expense_currency_exchange_account_id
        if not gain or not loss:
            raise UserError(_(
                "Configure the currency-exchange gain and loss accounts "
                "on company %(company)s before using FX auto write-off.",
                company=company.display_name,
            ))
        # Compute the residual on the statement line's auto-move so we
        # can pick the right account before delegating to the standard
        # write-off helper.
        move = statement_line.move_id
        suspense_lines = move.line_ids.filtered(
            lambda l: l.account_id.reconcile and not l.reconciled,
        )
        if not suspense_lines:
            raise UserError(_(
                "Cannot write off statement line %s: no reconcilable "
                "suspense line on its move.",
                statement_line.display_name,
            ))
        residual = sum(suspense_lines.mapped('amount_residual'))
        if max_amount is not None and abs(residual) > max_amount:
            raise UserError(_(
                "Residual %(amt).2f exceeds the FX auto-write-off cap "
                "of %(cap).2f. Use a manual write-off and capture a "
                "reason instead.",
                amt=residual, cap=max_amount,
            ))
        # residual > 0 means we still have a debit residual on a
        # receivable-style suspense; the bank received less than booked
        # so we recognise an exchange loss. residual < 0 means we
        # received more than booked, hence a gain.
        target_account = loss if residual > 0 else gain
        write_off_label = label or _("FX rounding write-off")
        self._perform_write_off(statement_line, target_account, write_off_label)
        self.env['eh.reconciliation.audit'].create({
            'session_id': self.id,
            'statement_line_id': statement_line.id,
            'aml_id': False,
            'user_id': self.env.user.id,
            'confidence': 1.0,
            'rules_fired': 'fx_writeoff',
            'decision': 'write_off',
            'source': 'manual',
        })
        self._increment_counters('write_offs')
        return True

    def apply_skip(self, statement_line_id):
        """Mark a statement line as deliberately skipped.

        Skip decisions do not perform any reconciliation; they just record
        that the user reviewed the line and chose to leave it for later.
        Useful for surfacing review backlog in audit reports.
        """
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_("Cannot skip on a closed session."))

        self.env['eh.reconciliation.audit'].create({
            'session_id': self.id,
            'statement_line_id': statement_line_id,
            'aml_id': False,
            'user_id': self.env.user.id,
            'confidence': 0.0,
            'rules_fired': '',
            'decision': 'skip',
            'source': 'manual',
        })
        self._increment_counters('skips')
        return True

    def _increment_counters(self, *fields_to_bump):
        """Atomically increment one or more session counters.

        The previous code did self.field += 1, which is read-modify-
        write at the ORM level: two concurrent calls could read the
        same value and both write the same incremented value, losing
        one increment. A direct SQL UPDATE column = column + 1 is
        atomic at the database level so concurrent decisions accumulate
        correctly. Field names are checked against an allowlist before
        being interpolated into SQL.
        """
        if not self:
            return
        validated = []
        for f in fields_to_bump:
            if f not in _ALLOWED_COUNTERS:
                raise ValueError(f"Counter {f!r} not in allowlist")
            validated.append(f)
        if not validated:
            return
        self.flush_recordset(validated)
        set_clause = SQL(', ').join(
            SQL("%s = %s + 1", SQL.identifier(f), SQL.identifier(f))
            for f in validated
        )
        self.env.cr.execute(SQL(
            "UPDATE eh_reconciliation_session SET %s WHERE id IN %s",
            set_clause, tuple(self.ids),
        ))
        self.invalidate_recordset(validated)

    # ---- workspace RPC ----

    @api.model
    def load_workspace(self, journal_id):
        """Load reconciliation workspace state for a journal.

        Opens (or reuses) a session for the current user on this journal,
        gathers unreconciled statement lines, and returns a flat dict the
        OWL workspace component can render directly.
        """
        session = self.open_or_create(journal_id)
        SLine = self.env['account.bank.statement.line']
        # In Odoo 19 the line's `date` is a non-stored related field
        # on move_id and cannot be used in the SQL ORDER BY. Order by
        # id descending: newest line first, matches the user's mental
        # model since ids on a journal grow with the import sequence.
        try:
            sl_records = SLine.search(
                [
                    ('journal_id', '=', journal_id),
                    ('is_reconciled', '=', False),
                ],
                limit=200, order='id desc',
            )
        except ValueError:
            # Older versions may not have is_reconciled as searchable;
            # fall back to a Python filter.
            sl_records = SLine.search(
                [('journal_id', '=', journal_id)],
                limit=400, order='id desc',
            ).filtered(lambda s: not getattr(s, 'is_reconciled', False))[:200]

        statement_lines = []
        for sl in sl_records:
            currency = sl.currency_id or sl.company_id.currency_id
            statement_lines.append({
                'id': sl.id,
                'date': sl.date.isoformat() if sl.date else None,
                'amount': sl.amount,
                'partner_id': sl.partner_id.id or False,
                'partner_name': sl.partner_id.name or '',
                'payment_ref': sl.payment_ref or '',
                'ref': sl.ref or '',
                'currency_code': currency.name if currency else '',
            })

        return {
            'session': self._serialize_session(session),
            'statement_lines': statement_lines,
        }

    @api.model
    def get_suggestions_for_line(self, statement_line_id, limit=10,
                                 threshold=0.3):
        """Return scored suggestions enriched with the AML fields the OWL
        widget needs to render each candidate.
        """
        statement_line = self.env['account.bank.statement.line'].browse(
            statement_line_id,
        ).exists()
        if not statement_line:
            return []
        engine = self.env['eh.reconciliation.suggestion.engine']
        raw = engine.find_suggestions(
            statement_line, limit=limit, threshold=threshold,
        )
        if not raw:
            return []
        aml_ids = [r['aml_id'] for r in raw]
        amls = self.env['account.move.line'].browse(aml_ids)
        aml_by_id = {a.id: a for a in amls}
        out = []
        for r in raw:
            aml = aml_by_id.get(r['aml_id'])
            if not aml:
                continue
            currency = aml.currency_id or aml.company_id.currency_id
            out.append({
                'aml_id': aml.id,
                'score': r['score'],
                'breakdown': r['breakdown'],
                'rules_fired': r['rules_fired'],
                'date': aml.date.isoformat() if aml.date else None,
                'partner_name': aml.partner_id.name or '',
                'amount_residual': aml.amount_residual,
                'currency_code': currency.name if currency else '',
                'move_name': aml.move_id.name or '',
                'ref': aml.ref or '',
                'label': aml.name or '',
            })
        return out

    @staticmethod
    def _serialize_session(session):
        return {
            'id': session.id,
            'name': session.name or '',
            'state': session.state,
            'opened_at': (
                session.opened_at.isoformat() if session.opened_at else None
            ),
            'matches_made': session.matches_made,
            'matches_via_suggestion': session.matches_via_suggestion,
            'matches_manual': session.matches_manual,
            'write_offs': session.write_offs,
            'skips': session.skips,
        }

    # ---- integration points ----

    def _perform_reconciliation(self, statement_line, aml_records):
        """Perform the actual reconciliation between a statement line and
        candidate AMLs. Wraps Odoo's standard reconciliation API.

        Override this method if you need to plug in a different
        reconciliation backend (custom journal entry creation, intercompany
        offsets, etc.).
        """
        # The statement line's move has reconcilable line(s) on a
        # receivable / payable / suspense account; reconcile those with
        # the candidate AMLs.
        move = statement_line.move_id
        sl_lines = move.line_ids.filtered(
            lambda l: l.account_id.reconcile,
        )
        if not sl_lines:
            return

        # Identify the suspense-account line(s) that carry the residual
        # that needs to be cleared. These are the lines on the statement
        # move that are NOT on the default bank account.
        journal = statement_line.journal_id
        bank_account = journal.default_account_id or journal.company_id.bank_account_root_id
        suspense_lines = sl_lines.filtered(
            lambda l: l.account_id != bank_account
        )
        # Cross-account reconciliation: create a bridging move that
        # transfers from the suspense account to each target AML's
        # account, then reconcile within each account separately.
        company_currency = move.company_id.currency_id

        for aml in aml_records:
            aml_residual = abs(aml.amount_residual)
            if company_currency.is_zero(aml_residual):
                continue

            suspense_line = suspense_lines[0] if suspense_lines else sl_lines[0]
            if suspense_line.credit > 0 and suspense_line.debit == 0:
                suspense_debit = aml_residual
                suspense_credit = 0.0
                target_debit = 0.0
                target_credit = aml_residual
            else:
                suspense_debit = 0.0
                suspense_credit = aml_residual
                target_debit = aml_residual
                target_credit = 0.0

            partner = aml.partner_id or statement_line.partner_id
            bridge_vals = {
                'journal_id': journal.id,
                'date': statement_line.date or fields.Date.today(),
                'ref': _("Reconcile: %s") % (statement_line.payment_ref or ''),
                'line_ids': [
                    (0, 0, {
                        'name': _("Bridge from %s") % (suspense_line.account_id.display_name or ''),
                        'account_id': suspense_line.account_id.id,
                        'debit': suspense_debit,
                        'credit': suspense_credit,
                        'partner_id': partner.id if partner else False,
                        'currency_id': company_currency.id,
                    }),
                    (0, 0, {
                        'name': _("Bridge to %s") % (aml.account_id.display_name or ''),
                        'account_id': aml.account_id.id,
                        'debit': target_debit,
                        'credit': target_credit,
                        'partner_id': partner.id if partner else False,
                        'currency_id': company_currency.id,
                    }),
                ],
            }
            bridge_move = self.env['account.move'].create(bridge_vals)
            bridge_move.action_post()

            # Reconcile within each account.
            # 1. Suspense: old suspense line(s) + new bridge suspense line
            bridge_suspense = bridge_move.line_ids.filtered(
                lambda l: l.account_id == suspense_line.account_id
            )
            all_suspense = suspense_lines + bridge_suspense
            if len(all_suspense) >= 2:
                all_suspense.filtered(
                    lambda l: l.account_id.reconcile
                ).reconcile()

            # 2. Target account: AML + bridge target line
            bridge_target = bridge_move.line_ids.filtered(
                lambda l: l.account_id == aml.account_id
            )
            target_lines = aml + bridge_target
            if len(target_lines) >= 2:
                target_lines.filtered(
                    lambda l: l.account_id.reconcile
                ).reconcile()

    def _perform_write_off(self, statement_line, account, label):
        """Create a standalone write-off entry and reconcile it with the
        statement line's suspense line.

        The statement line's auto-generated move (Bank / Suspense) is left
        untouched.  A separate journal entry is created:

          Residual > 0 (suspense had a net debit):
            Dr target account  /  Cr suspense
          Residual < 0 (suspense had a net credit):
            Cr target account  /  Dr suspense

        The new entry's suspense side is then reconciled with the
        statement line's original suspense line, clearing both.
        """
        move = statement_line.move_id
        journal = statement_line.journal_id
        suspense_account = journal.suspense_account_id
        suspense_lines = move.line_ids.filtered(
            lambda l: l.account_id == suspense_account and not l.reconciled,
        )
        if not suspense_lines:
            raise UserError(_(
                "Cannot write off statement line %s: it has no "
                "reconcilable suspense line on its journal move. "
                "Verify the bank journal's suspense account is set "
                "and the statement line was processed normally.",
                statement_line.display_name,
            ))
        residual = sum(suspense_lines.mapped('amount_residual'))
        if move.company_id.currency_id.is_zero(residual):
            raise UserError(_(
                "Cannot write off statement line %s: residual is "
                "already zero.",
                statement_line.display_name,
            ))

        write_off_label = label or _("Write-off")
        abs_residual = abs(residual)

        write_off_move = self.env['account.move'].create({
            'journal_id': journal.id,
            'date': statement_line.date,
            'ref': '%s: %s' % (statement_line.display_name, write_off_label),
            'line_ids': [
                (0, 0, {
                    'name': write_off_label,
                    'account_id': account.id,
                    'debit': abs_residual if residual > 0 else 0.0,
                    'credit': abs_residual if residual < 0 else 0.0,
                    'partner_id': statement_line.partner_id.id,
                }),
                (0, 0, {
                    'name': write_off_label,
                    'account_id': suspense_account.id,
                    'debit': abs_residual if residual < 0 else 0.0,
                    'credit': abs_residual if residual > 0 else 0.0,
                    'partner_id': statement_line.partner_id.id,
                }),
            ],
        })
        write_off_move.action_post()

        new_suspense_line = write_off_move.line_ids.filtered(
            lambda l: l.account_id == suspense_account,
        )
        (suspense_lines + new_suspense_line).filtered(
            lambda l: l.account_id.reconcile,
        ).reconcile()
        return True
