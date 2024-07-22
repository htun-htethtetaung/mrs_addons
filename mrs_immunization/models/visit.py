from odoo import models, fields


class Visit(models.Model):
    _inherit = "mrs.visit"

    immunization_ids = fields.One2many(
        comodel_name="mrs.visit.immunization", inverse_name="visit_id", tracking=True
    )
