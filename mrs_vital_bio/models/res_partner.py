from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    vital_ids = fields.One2many(comodel_name="mrs.vital", inverse_name="patient_id")
    biometric_ids = fields.One2many(
        comodel_name="mrs.biometric", inverse_name="patient_id"
    )
