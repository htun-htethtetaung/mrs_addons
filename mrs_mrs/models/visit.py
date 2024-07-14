from datetime import datetime
from odoo import fields, models, api


class Visit(models.Model):
    _name = "mrs.visit"

    _description = "Visit to patient"

    _inherits = {}
    _inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]

    patient_id = fields.Many2one(comodel_name="res.partner")
    doctor_id = fields.Many2one(
        comodel_name="res.users", default=lambda x: x.env.user.id
    )
    is_external_doctor = fields.Boolean(default=False)
    external_doctor_name = fields.Char(size=30)
    start_date = fields.Datetime(default=lambda x: datetime.now(), index=True)
    end_date = fields.Datetime(readonly=True)
    mrs_location_id = fields.Many2one(comodel_name="mrs.location")

    # Prescription
    prescription_order_ids = fields.One2many(
        comodel_name="mrs.prescription.order", inverse_name="visit_id"
    )
    prescription_lab_ids = fields.One2many(
        comodel_name="mrs.prescription.lab", inverse_name="visit_id"
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
