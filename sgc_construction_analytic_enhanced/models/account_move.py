from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    construction_project_id = fields.Many2one(
        "construction.project",
        string="Construction Project",
        compute="_compute_construction_project_id",
        store=True,
        index=True,
        search="_search_construction_project",
        help="Construction project linked via analytic distribution on invoice lines",
    )

    @api.depends("line_ids.analytic_distribution")
    def _compute_construction_project_id(self):
        analytic_projects = self.env["construction.project"].search([
            ("analytic_account_id", "!=", False),
        ])
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
        if operator not in ("=", "!=", "in", "not in", "child_of"):
            return [("id", "=", False)]

        if value:
            projects = self.env["construction.project"].browse(value)
            analytic_ids = projects.mapped("analytic_account_id").ids
            if not analytic_ids:
                return [("id", "=", False)]
            return [("line_ids.analytic_distribution", "in", analytic_ids)]
        else:
            all_projects = self.env["construction.project"].search([
                ("analytic_account_id", "!=", False),
            ])
            all_analytic_ids = all_projects.mapped("analytic_account_id").ids
            if not all_analytic_ids:
                return []
            return [("line_ids.analytic_distribution", "not in", all_analytic_ids)]

    def action_view_construction_project(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Construction Project",
            "res_model": "construction.project",
            "view_mode": "form",
            "res_id": self.construction_project_id.id,
            "target": "current",
        }


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    construction_project_id = fields.Many2one(
        "construction.project",
        string="Project",
        related="move_id.construction_project_id",
        store=True,
        index=True,
        help="Construction project linked via analytic distribution on the parent invoice",
    )
