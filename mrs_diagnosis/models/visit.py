from odoo import models, fields


class Visit(models.Model):
    _inherit = "mrs.visit"

    condition_ids = fields.One2many(
        comodel_name="mrs.diagnosis.condition", inverse_name="visit_id"
    )
