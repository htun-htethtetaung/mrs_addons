# pylint: disable=no-member
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    program_ids = fields.One2many(
        comodel_name="mrs.visit.program", inverse_name="patient_id"
    )

    def action_view_partner_program(self):
        return self._action_partner_visit("mrs_program.mrs_visit_program_action")
