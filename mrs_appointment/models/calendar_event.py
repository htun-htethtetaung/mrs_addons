# pylint: disable=no-member
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from ...mrs_mrs.models.visit import VisitStatus


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    patient_id = fields.Many2one(
        comodel_name="res.partner", index=True, domain="[('is_patient', '=', True)]"
    )
    current_visit = fields.Many2one(
        comodel_name="mrs.visit", related="patient_id.current_visit"
    )
    is_patient_appointment = fields.Boolean(
        related="appointment_type_id.is_patient_appointment"
    )
    visit_id = fields.Many2one(comodel_name="mrs.visit", index=True)
    is_appointment_done = fields.Boolean(compute="_compute_is_appointment_done")

    @api.depends("visit_id")
    def _compute_is_appointment_done(self):
        for record in self:
            if record.visit_id:
                record.is_appointment_done = (
                    record.visit_id.state == VisitStatus.ENDED.name
                )
            else:
                record.is_appointment_done = False

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.partner_ids = [(4, record.patient_id.id)]

    def create_new_visit(self):
        self.ensure_one()
        return self.env["mrs.visit"].create(
            {"patient_id": self.patient_id.id, "calendar_event_id": self.id}
        )

    def action_go_to_current_visit(self):
        self.ensure_one()
        if not self.patient_id:
            raise ValidationError(_("Patient ID is required"))
        if self.visit_id:
            return self.visit_id.action_go_to_visit()
        if self.current_visit:
            self.visit_id = self.current_visit.id
            self.visit_id.calendar_event_id = self.id
            return self.visit_id.action_go_to_visit()
        new_visit = self.create_new_visit()
        self.visit_id = new_visit.id
        return new_visit.action_go_to_visit()
