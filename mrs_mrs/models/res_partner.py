# pylint: disable=no-member,protected-access
from odoo import fields, models

IR_ACT_WINDOW = "ir.actions.act_window"


class ResPartner(models.Model):
    _inherit = "res.partner"

    visit_ids = fields.One2many(comodel_name="mrs.visit", inverse_name="patient_id")
    current_visit = fields.Many2one(
        comodel_name="mrs.visit", compute="_compute_is_active_visit"
    )
    doctor_ids = fields.Many2many(
        comodel_name="res.users",
        relation="patient_doctor_relation",
        column1="patient_id",
        column2="doctor_id",
        index=True,
    )

    def _compute_is_active_visit(self):
        for record in self:
            record.current_visit = self.env["mrs.visit"].get_current_visit(
                patient_id=record.id
            )

    def action_go_to_current_visit(self):
        self.ensure_one()
        context = {**self._context, "default_patient_id": self.id}
        action = {
            "type": IR_ACT_WINDOW,
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mrs.visit",
            "domain": [("patient_id", "=", self.id)],
            "context": context,
        }
        if self.current_visit:
            action["res_id"] = self.current_visit.id
        return action

    def _action_partner_visit(self, view_name: str):
        action = self.env["ir.actions.actions"]._for_xml_id(view_name)
        action["domain"] = [("patient_id", "=", self.id)]
        action["context"] = {"default_patient_id": self.id}
        return action

    def action_view_partner_visits(self):
        return self._action_partner_visit("mrs_mrs.mrs_visit_action")

    def action_go_to_contact(self):
        return {
            "type": IR_ACT_WINDOW,
            "view_type": "form",
            "view_mode": "form",
            "res_model": self._name,
            "res_id": self.id,
        }
