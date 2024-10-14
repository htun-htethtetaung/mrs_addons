from odoo import models, fields, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    condition_ids = fields.One2many(
        comodel_name="mrs.diagnosis.condition", inverse_name="visit_id"
    )

    condition_history = fields.Many2many(
        compute="_compute_condition_history", comodel_name="mrs.diagnosis.condition"
    )

    @api.depends("patient_id")
    def _compute_condition_history(self):
        for record in self:
            records = self.env["mrs.diagnosis.condition"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.condition_history = records
