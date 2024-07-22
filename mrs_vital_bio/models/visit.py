from odoo import models, fields


class Visit(models.Model):
    _inherit = "mrs.visit"

    vital_ids = fields.One2many(
        comodel_name="mrs.vital", inverse_name="visit_id", tracking=True
    )

    biometric_ids = fields.One2many(
        comodel_name="mrs.biometric", inverse_name="visit_id", tracking=True
    )
