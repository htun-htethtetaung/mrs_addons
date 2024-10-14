from odoo import models, fields, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    allergy_line_ids = fields.One2many(
        comodel_name="mrs.allergy", inverse_name="visit_id"
    )
    allergy_history = fields.Many2many(
        compute="_compute_allergy_history", comodel_name="mrs.allergy"
    )

    @api.depends("patient_id")
    def _compute_allergy_history(self):
        for record in self:
            records = self.env["mrs.allergy"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.allergy_history = records
