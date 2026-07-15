# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    construction_project_id = fields.Many2one(
        'construction.project',
        string='Project',
        compute='_compute_construction_project_id',
        store=True,
        index=True,
        search='_search_construction_project',
        help='Construction project linked via analytic distribution on invoice lines',
    )

    @api.depends('line_ids.analytic_distribution')
    def _compute_construction_project_id(self):
        """Resolve the construction project from analytic distribution on invoice lines.

        Logic:
        - Collect all analytic account IDs from all invoice lines
        - Find construction.project records matching those analytic accounts
        - If exactly one project matches → assign it
        - If multiple projects match → leave empty (ambiguous)
        """
        analytic_projects = self.env['construction.project'].search([
            ('analytic_account_id', '!=', False),
        ])
        # Build a lookup: analytic_account_id → project
        analytic_to_project = {
            p.analytic_account_id.id: p.id
            for p in analytic_projects
        }

        for move in self:
            project_ids = set()
            for line in move.line_ids:
                distribution = line.analytic_distribution or {}
                for analytic_id_str in distribution:
                    try:
                        analytic_id = int(analytic_id_str)
                        if analytic_id in analytic_to_project:
                            project_ids.add(analytic_to_project[analytic_id])
                    except (TypeError, ValueError):
                        continue

            if len(project_ids) == 1:
                move.construction_project_id = project_ids.pop()
            else:
                move.construction_project_id = False

    def _search_construction_project(self, operator, value):
        """Allow searching invoices by construction project."""
        if operator not in ('=', '!=', 'in', 'not in', 'child_of'):
            return [('id', '=', False)]

        # Find analytic account IDs for the given project(s)
        if value:
            projects = self.env['construction.project'].browse(value)
            analytic_ids = projects.mapped('analytic_account_id').ids
            if not analytic_ids:
                return [('id', '=', False)]
            # Search for moves that have any line with matching analytic distribution
            return [('line_ids.analytic_distribution', 'in', analytic_ids)]
        else:
            # Searching for empty — moves with no construction project
            all_projects = self.env['construction.project'].search([
                ('analytic_account_id', '!=', False),
            ])
            all_analytic_ids = all_projects.mapped('analytic_account_id').ids
            if not all_analytic_ids:
                return []
            return [('line_ids.analytic_distribution', 'not in', all_analytic_ids)]

    def action_view_construction_project(self):
        """Smart button: open the linked construction project."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Construction Project',
            'res_model': 'construction.project',
            'view_mode': 'form',
            'res_id': self.construction_project_id.id,
            'target': 'current',
        }


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    construction_project_id = fields.Many2one(
        'construction.project',
        string='Project',
        related='move_id.construction_project_id',
        store=True,
        index=True,
        help='Construction project linked via analytic distribution on the parent invoice',
    )
