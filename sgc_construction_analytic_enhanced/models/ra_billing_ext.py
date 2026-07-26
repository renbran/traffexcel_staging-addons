# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionRABilling(models.Model):
    _inherit = "construction.ra.billing"

    def action_print_combined_soa(self):
        """Print combined SOA PDF for selected RA Billings."""
        return self.env.ref("sgc_construction_analytic_enhanced.action_report_combined_soa").report_action(self)