# pylint: disable=no-member
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    condition_ids = fields.One2many(
        comodel_name="mrs.diagnosis.condition", inverse_name="patient_id"
    )

    def action_view_partner_diagnosis(self):
        return self._action_partner_visit(
            "mrs_diagnosis.mrs_diagnosis_condition_action"
        )
