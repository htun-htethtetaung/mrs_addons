from datetime import datetime
from enum import Enum
from odoo import fields, models, api


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

    _inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]

    patient_id = fields.Many2one(comodel_name="res.partner", tracking=True)
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

    # Prescription
    prescription_order_ids = fields.One2many(
        comodel_name="mrs.prescription.order", inverse_name="visit_id", tracking=True
    )
    prescription_lab_ids = fields.One2many(
        comodel_name="mrs.prescription.lab", inverse_name="visit_id", tracking=True
    )

    vital_ids = fields.One2many(
        comodel_name="mrs.vital", inverse_name="visit_id", tracking=True
    )

    biometric_ids = fields.One2many(
        comodel_name="mrs.biometric", inverse_name="visit_id", tracking=True
    )

    condition_ids = fields.One2many(
        comodel_name="mrs.diagnosis.condition", inverse_name="visit_id"
    )

    @api.onchange("doctor_id")
    def onchange_doctor_id(self):
        for record in self:
            if record.doctor_id:
                record.mrs_location_id = record.doctor_id.default_mrs_location_id.id

    @api.onchange("is_external_doctor")
    def onchange_is_external_doctor(self):
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
