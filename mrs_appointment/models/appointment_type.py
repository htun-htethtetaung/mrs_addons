from odoo import fields, models


class AppointmentType(models.Model):
    _inherit = "appointment.type"

    is_patient_appointment = fields.Boolean(default=True)
