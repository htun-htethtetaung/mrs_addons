# pylint: disable=no-member
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    prescription_ids = fields.One2many(
        comodel_name="mrs.prescription.order", inverse_name="patient_id"
    )

    def action_view_partner_prescription(self):
        return self._action_partner_visit(
            "mrs_prescription.mrs_prescription_order_action"
        )
