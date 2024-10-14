from odoo import models, fields, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    program_ids = fields.One2many(
        comodel_name="mrs.visit.program", inverse_name="visit_id", tracking=True
    )

    program_history = fields.Many2many(
        compute="_compute_program_history", comodel_name="mrs.visit.program"
    )

    @api.depends("patient_id")
    def _compute_program_history(self):
        for record in self:
            records = self.env["mrs.visit.program"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.program_history = records
