# pylint: disable=no-member
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    lab_ids = fields.One2many(comodel_name="mrs.lab", inverse_name="patient_id")

    def action_view_partner_lab(self):
        return self._action_partner_visit("mrs_lab.mrs_lab_action")
