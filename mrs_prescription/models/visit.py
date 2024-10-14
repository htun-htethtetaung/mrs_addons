from odoo import fields, models, api


class Visit(models.Model):
    _inherit = "mrs.visit"

    prescription_order_ids = fields.One2many(
        comodel_name="mrs.prescription.order", inverse_name="visit_id", tracking=True
    )

    prescription_history = fields.Many2many(
        compute="_compute_prescription_history", comodel_name="mrs.prescription.order"
    )

    @api.depends("patient_id")
    def _compute_prescription_history(self):
        for record in self:
            records = self.env["mrs.prescription.order"].search(
                [
                    ("patient_id", "=", record.patient_id.id),
                    ("visit_id", "!=", record.id),
                ]
            )
            record.prescription_history = records
