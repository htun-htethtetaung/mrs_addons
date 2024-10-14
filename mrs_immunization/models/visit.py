from odoo import models, fields, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    immunization_ids = fields.One2many(
        comodel_name="mrs.visit.immunization", inverse_name="visit_id", tracking=True
    )

    immunization_history = fields.Many2many(
        compute="_compute_immunization_history", comodel_name="mrs.visit.immunization"
    )

    @api.depends("patient_id")
    def _compute_immunization_history(self):
        for record in self:
            records = self.env["mrs.visit.immunization"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.immunization_history = records
