from odoo import models, fields


class Visit(models.Model):
    _inherit = "mrs.visit"

    allergy_line_ids = fields.One2many(
        comodel_name="mrs.allergy", inverse_name="visit_id"
    )
