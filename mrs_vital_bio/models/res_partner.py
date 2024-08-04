# pylint: disable=no-member
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    vital_ids = fields.One2many(comodel_name="mrs.vital", inverse_name="patient_id")
    biometric_ids = fields.One2many(
        comodel_name="mrs.biometric", inverse_name="patient_id"
    )

    def action_view_partner_vitals(self):
        return self._action_partner_visit("mrs_vital_bio.mrs_vital_action")

    def action_view_partner_biometrics(self):
        return self._action_partner_visit("mrs_vital_bio.mrs_biometric_action")
