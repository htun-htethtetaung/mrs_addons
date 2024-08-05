# pylint: disable=no-member
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    allergy_ids = fields.One2many(comodel_name="mrs.allergy", inverse_name="patient_id")

    def action_view_partner_allergy(self):
        return self._action_partner_visit("mrs_allergy.mrs_allergy_action")
