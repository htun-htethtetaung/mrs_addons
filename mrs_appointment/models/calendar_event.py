# pylint: disable=no-member
from odoo import fields, models, api


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    patient_id = fields.Many2one(comodel_name="res.partner", index=True)
    current_visit = fields.Many2one(
        comodel_name="mrs.visit", related="patient_id.current_visit"
    )
    is_patient_appointment = fields.Boolean(
        related="appointment_type_id.is_patient_appointment"
    )

    @api.onchange("patient_id")
    def _onchange_patient_id(self):
        for record in self:
            if record.patient_id:
                record.partner_ids = [(6, 0, [record.patient_id.id])]

    def action_go_to_current_visit(self):
        self.ensure_one()
        if self.current_visit:
            self.current_visit.calendar_event_id = self.id
        return self.patient_id.with_context(
            default_calendar_event_id=self.id
        ).action_go_to_current_visit()
