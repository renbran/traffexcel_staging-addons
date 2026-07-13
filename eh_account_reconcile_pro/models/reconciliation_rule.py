# -*- encoding: utf-8 -*-
##############################################################################
#
# ERP Heritage
# Copyright (C) 2026 (https://www.erpheritage.com.au/)
#
##############################################################################
"""
User-defined reconciliation rules.

The free heuristic engine in suggestion_engine.py scores candidates from
five signals (amount, date, partner, reference, history). Rules go a step
further: a manager defines a deterministic pattern that, when matched,
either auto-confirms a match or produces a high-confidence suggestion
the user can accept with one click.

Typical rule examples:

* "Bank fee under 10 dollars referenced as 'FEE' is a write off to the
  Bank Charges account."
* "Payment ref matching ^INV-\\d{6}$ between 100 and 50000 dollars
  matches receivable AML by amount and partner."
* "Anything credited from journal X partner Y always goes to expense
  account Z."

Rules are evaluated AFTER the heuristic engine. A rule that fires raises
the score by `score_boost` (default 0.5) and tags `rules_fired` with the
rule's code so the audit trail records which rule confirmed the match.

Sequence drives evaluation order. The first rule to fully match wins for
auto-confirm rules; suggestion-only rules can stack their boosts.
"""

import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


_CODE_RE = re.compile(r'^[a-z][a-z0-9_]*$')


class EhReconciliationRule(models.Model):
    _name = 'eh.reconciliation.rule'
    _description = "Bank reconciliation rule"
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    code = fields.Char(
        required=True, copy=False,
        help="Stable identifier surfaced in the audit log when the rule fires.",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        'res.company', required=True,
        default=lambda self: self.env.company,
    )

    # ---- scope: when does this rule apply ----

    journal_ids = fields.Many2many(
        'account.journal',
        'eh_recon_rule_journal_rel',
        'rule_id', 'journal_id',
        domain="[('type', 'in', ['bank', 'cash'])]",
        help="Limit this rule to specific bank or cash journals. Empty means all bank/cash journals in the company.",
    )

    rule_type = fields.Selection(
        [
            ('match', "Suggest a match against a journal item"),
            ('write_off', "Auto write-off to a fixed account"),
        ],
        required=True, default='match',
    )

    # ---- pattern matching against the statement line ----

    payment_ref_regex = fields.Char(
        string="Payment ref regex",
        help="Optional. Statement line payment_ref must match this regex (Python re syntax). Anchored with ^ and $ if you want full match.",
    )
    narration_regex = fields.Char(
        string="Narration regex",
        help="Optional. Statement line narration must match this regex.",
    )
    amount_min = fields.Float(
        digits=(16, 2),
        help="Optional. Statement line absolute amount must be >= this. Leave 0 for no lower bound.",
    )
    amount_max = fields.Float(
        digits=(16, 2),
        help="Optional. Statement line absolute amount must be <= this. Leave 0 for no upper bound.",
    )
    direction = fields.Selection(
        [
            ('any', "Any"),
            ('credit', "Credit only (money in)"),
            ('debit', "Debit only (money out)"),
        ],
        default='any', required=True,
    )

    # ---- write-off target ----

    writeoff_account_id = fields.Many2one(
        'account.account',
        help="Required for write-off rules. The account the residual is written off to.",
    )
    writeoff_label = fields.Char(
        translate=True,
        help="Label written on the write-off journal item.",
    )

    # ---- match boost ----

    partner_id = fields.Many2one(
        'res.partner',
        help="Optional. When set, the rule only suggests AMLs for this partner.",
    )
    score_boost = fields.Float(
        default=0.5, digits=(3, 2),
        help="Confidence boost added to the suggestion score when this rule fires (range 0.0 to 1.0).",
    )
    auto_confirm = fields.Boolean(
        default=False,
        help="When enabled, a suggestion produced by this rule is auto-confirmed instead of waiting for a user click. Use sparingly: requires high pattern specificity.",
    )

    # ---- audit ----

    fire_count = fields.Integer(
        default=0, readonly=True,
        help="Total number of times this rule has fired across all sessions.",
    )
    last_fired_at = fields.Datetime(readonly=True)

    notes = fields.Text()

    _unique_code_company = models.Constraint(
        'unique(code, company_id)',
        'Rule code must be unique per company.',
    )
    _check_score_boost = models.Constraint(
        'CHECK (score_boost >= 0 AND score_boost <= 1)',
        'Score boost must be between 0.0 and 1.0.',
    )
    _check_amounts = models.Constraint(
        'CHECK ((amount_min = 0 AND amount_max = 0) OR amount_min <= amount_max OR amount_max = 0)',
        'amount_max must be greater than or equal to amount_min when both are set.',
    )

    @api.constrains('code')
    def _check_code_format(self):
        for rec in self:
            if not _CODE_RE.match(rec.code or ''):
                raise ValidationError(_(
                    "Rule code must match [a-z][a-z0-9_]* (got %r).",
                ) % rec.code)

    @api.constrains('rule_type', 'writeoff_account_id', 'active')
    def _check_writeoff_target(self):
        for rec in self:
            if rec.active and rec.rule_type == 'write_off' and not rec.writeoff_account_id:
                raise ValidationError(_(
                    "Active write-off rules require a writeoff_account_id.",
                ))

    @api.constrains('payment_ref_regex', 'narration_regex')
    def _check_regex(self):
        for rec in self:
            for value, label in (
                (rec.payment_ref_regex, 'payment_ref_regex'),
                (rec.narration_regex, 'narration_regex'),
            ):
                if not value:
                    continue
                try:
                    re.compile(value)
                except re.error as exc:
                    raise ValidationError(_(
                        "%(label)s is not a valid Python regex: %(err)s",
                        label=label, err=str(exc),
                    ))

    # ---- evaluation ----

    def matches_statement_line(self, statement_line):
        """Return True if this rule's filters match the given statement line.

        Pure read; does not mutate state. Caller decides what to do with
        the match (suggest, write off, auto confirm).
        """
        self.ensure_one()
        if not self.active:
            return False
        if statement_line.company_id != self.company_id:
            return False
        if self.journal_ids and statement_line.journal_id not in self.journal_ids:
            return False
        amount = abs(statement_line.amount or 0.0)
        if self.amount_min and amount < self.amount_min:
            return False
        if self.amount_max and amount > self.amount_max:
            return False
        if self.direction == 'credit' and (statement_line.amount or 0.0) < 0:
            return False
        if self.direction == 'debit' and (statement_line.amount or 0.0) > 0:
            return False
        if self.payment_ref_regex:
            if not statement_line.payment_ref:
                return False
            if not re.search(self.payment_ref_regex, statement_line.payment_ref):
                return False
        if self.narration_regex:
            narration = statement_line.narration or ''
            if not re.search(self.narration_regex, narration):
                return False
        return True

    def record_fire(self):
        """Bump the fire counter atomically.

        Atomic counter increments protect against the read-modify-write
        race that would otherwise lose increments under concurrent
        reconciliation activity. Mirrors the pattern in
        eh.reconciliation.session._increment_counters.
        """
        if not self:
            return
        from odoo.tools import SQL
        self.flush_recordset(['fire_count'])
        self.env.cr.execute(SQL(
            "UPDATE eh_reconciliation_rule "
            "SET fire_count = fire_count + 1, "
            "    last_fired_at = NOW() AT TIME ZONE 'UTC' "
            "WHERE id IN %s",
            tuple(self.ids),
        ))
        self.invalidate_recordset(['fire_count', 'last_fired_at'])
