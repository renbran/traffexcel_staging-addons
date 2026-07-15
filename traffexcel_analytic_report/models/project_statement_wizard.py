# -*- coding: utf-8 -*-
from odoo import fields, models


class ProjectStatementWizard(models.TransientModel):
    """Options for the Project Statement (XLSX) download.

    The wizard is a thin shim: it collects the user's choices and forwards
    them as URL query parameters to ``/traffexcel/project_statement/xlsx``
    (handled in ``controllers/main.py``). Keeping the route bookmarkable means
    the URL stays linkable from audit logs and reports even after the
    wizard is removed.
    """

    _name = "traffexcel.project.statement.wizard"
    _description = "Project Statement (XLSX) options"

    date_from = fields.Date(string="From")
    date_to = fields.Date(string="To")
    vat_mode = fields.Selection(
        [
            ("excl", "Exclude VAT"),
            ("incl", "Include VAT"),
            ("both", "Show Excl. / VAT / Incl."),
        ],
        string="VAT display",
        default="both",
        required=True,
    )
    entry_state = fields.Selection(
        [
            ("all", "Draft + Posted"),
            ("posted", "Posted only"),
            ("draft", "Draft only"),
        ],
        string="Entries",
        default="all",
        required=True,
        help=(
            "Filter by the state of the source invoice/journal entry. "
            "Lines without a source entry (manual analytic lines) are "
            "always excluded from Draft-only and Posted-only filters."
        ),
    )

    def action_download_xlsx(self):
        """Forward to the XLSX controller with the wizard's choices as params."""
        self.ensure_one()
        params = {
            "vat_mode": self.vat_mode,
            "entry_state": self.entry_state,
        }
        if self.date_from:
            params["date_from"] = self.date_from
        if self.date_to:
            params["date_to"] = self.date_to
        url = "/traffexcel/project_statement/xlsx?" + "&".join(
            "%s=%s" % (k, v) for k, v in params.items()
        )
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "new",
        }