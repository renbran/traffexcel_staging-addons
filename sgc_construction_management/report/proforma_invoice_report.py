# -*- coding: utf-8 -*-
from odoo import api, models, _


class ProformaInvoiceReport(models.AbstractModel):
    _name = "report.sgc_construction_management.report_proforma_invoice"
    _description = "RA Billing Proforma Invoice Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["construction.ra.billing"].browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": "construction.ra.billing",
            "docs": docs,
        }