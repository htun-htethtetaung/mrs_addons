# pylint: disable=no-member,protected-access
from odoo import fields, models

IR_ACT_WINDOW = "ir.actions.act_window"


class ResPartner(models.Model):
    _inherit = "res.partner"

    visit_ids = fields.One2many(comodel_name="mrs.visit", inverse_name="patient_id")
    current_visit = fields.Many2one(
        comodel_name="mrs.visit", compute="_compute_is_active_visit"
    )

    def _compute_is_active_visit(self):
        for record in self:
            record.current_visit = self.env["mrs.visit"].get_current_visit(
                patient_id=record.id
            )

    def action_go_to_current_visit(self):
        self.ensure_one()
        action = {
            "type": IR_ACT_WINDOW,
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mrs.visit",
            "domain": [("patient_id", "=", self.id)],
            "context": {"default_patient_id": self.id},
        }
        if self.current_visit:
            action["res_id"] = self.current_visit.id
        return action

    def action_view_partner_visits(self):
        action = self.env["ir.actions.actions"]._for_xml_id("mrs_mrs.mrs_visit_action")
        action["domain"] = [("patient_id", "=", self.id)]
        action["context"] = {"default_patient_id": self.id}
        return action
