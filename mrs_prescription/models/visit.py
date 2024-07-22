from odoo import fields, models


class Visit(models.Model):
    _inherit = "mrs.visit"

    prescription_order_ids = fields.One2many(
        comodel_name="mrs.prescription.order", inverse_name="visit_id", tracking=True
    )
