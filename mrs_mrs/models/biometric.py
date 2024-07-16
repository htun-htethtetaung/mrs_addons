from datetime import datetime
from odoo import fields, models


class Biometric(models.Model):
    _name = "mrs.biometric"

    _description = "Biometric Data"

    visit_id = fields.Many2one(comodel_name="mrs.visit", index=True)
    patient_id = fields.Many2one(
        comodel_name="res.partner", index=True, related="visit_id.patient_id"
    )
    recorded_date = fields.Datetime(index=True, default=lambda x: datetime.now())
    weight = fields.Float(string="Weight (kg)")
    height = fields.Float(string="Height (cm)")
    bmi = fields.Float(string="BMI (kg/m^2)")
    muac = fields.Float(string="MUAC (cm)")
