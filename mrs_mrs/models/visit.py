from datetime import datetime
from enum import Enum
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class VisitStatus(Enum):
    DRAFT = "Draft"
    START = "Started"
    ENDED = "Ended"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)


class Visit(models.Model):
    _name = "mrs.visit"

    _description = "Visit to patient"

    _order = "start_date DESC"

    _inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]

    patient_id = fields.Many2one(
        index=True,
        comodel_name="res.partner",
        required=True,
        tracking=True,
        domain="[('is_patient', '=', True)]",
    )
    name = fields.Char(related="patient_id.name")
    doctor_id = fields.Many2one(
        comodel_name="res.users", default=lambda x: x.env.user.id
    )
    state = fields.Selection(
        selection=list(VisitStatus.name_value()),
        index=True,
        default=VisitStatus.DRAFT.name,
        tracking=True,
    )
    is_external_doctor = fields.Boolean(default=False)
    external_doctor_name = fields.Char(size=30)
    start_date = fields.Datetime(
        default=lambda x: datetime.now(), index=True, tracking=True
    )
    end_date = fields.Datetime(readonly=True)
    mrs_location_id = fields.Many2one(comodel_name="mrs.location")

    note = fields.Text(tracking=True)

    @api.constrains("patient_id", "state")
    def _open_visit_per_patient(self):
        for record in self:
            if record.patient_id and self.search_count(
                [
                    ("id", "!=", record.id),
                    ("patient_id", "=", record.patient_id.id),
                    ("state", "=", VisitStatus.START.name),
                ]
            ):
                raise ValidationError(_("Please end the previous started visit!"))

    @api.onchange("doctor_id")
    def _onchange_doctor_id(self):
        for record in self:
            if record.doctor_id:
                record.mrs_location_id = record.doctor_id.default_mrs_location_id.id

    @api.onchange("is_external_doctor")
    def _onchange_is_external_doctor(self):
        for record in self:
            if record.is_external_doctor:
                record.doctor_id = None

    def action_start(self):
        for record in self:
            record.state = VisitStatus.START.name
            record.start_date = (
                record.start_date if record.start_date else datetime.now()
            )

    def action_end(self):
        for record in self:
            record.state = VisitStatus.ENDED.name
            record.end_date = record.end_date if record.end_date else datetime.now()
