from odoo import models, fields, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    lab_ids = fields.One2many(
        comodel_name="mrs.lab", inverse_name="visit_id", tracking=True
    )
    lab_history = fields.Many2many(
        compute="_compute_lab_history", comodel_name="mrs.lab"
    )

    @api.depends("patient_id")
    def _compute_lab_history(self):
        for record in self:
            records = self.env["mrs.lab"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.lab_history = records
