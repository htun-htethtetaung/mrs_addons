from odoo import models, fields


class Visit(models.Model):
    _inherit = "mrs.visit"

    lab_ids = fields.One2many(
        comodel_name="mrs.lab", inverse_name="visit_id", tracking=True
    )
