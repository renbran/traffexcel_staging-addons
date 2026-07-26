# -*- coding: utf-8 -*-
from odoo import api, models, _


class CombinedSOAReport(models.AbstractModel):
    _name = "report.sgc_construction_analytic_enhanced.report_combined_soa"
    _description = "Combined SOA for RA Billings"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["construction.ra.billing"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "construction.ra.billing",
            "docs": docs,
        }