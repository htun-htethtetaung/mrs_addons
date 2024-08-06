# pylint: disable=no-member
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    immunization_ids = fields.One2many(
        comodel_name="mrs.visit.immunization", inverse_name="patient_id"
    )

    def action_view_partner_visit_immunization(self):
        return self._action_partner_visit(
            "mrs_immunization.mrs_visit_immunization_action"
        )
