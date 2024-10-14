from odoo import models, fields, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    vital_ids = fields.One2many(
        comodel_name="mrs.vital", inverse_name="visit_id", tracking=True
    )

    vital_history = fields.Many2many(
        compute="_compute_vital_history", comodel_name="mrs.vital"
    )

    biometric_ids = fields.One2many(
        comodel_name="mrs.biometric", inverse_name="visit_id", tracking=True
    )

    bio_history = fields.Many2many(
        compute="_compute_bio_history", comodel_name="mrs.biometric"
    )

    @api.depends("patient_id")
    def _compute_vital_history(self):
        for record in self:
            records = self.env["mrs.vital"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.vital_history = records

    @api.depends("patient_id")
    def _compute_bio_history(self):
        for record in self:
            records = self.env["mrs.biometric"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.bio_history = records
