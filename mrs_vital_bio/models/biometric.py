from datetime import datetime
from odoo import fields, models


class Biometric(models.Model):
    _name = "mrs.biometric"

    _inherit = "mrs.visit.line.abstract"

    _order = "recorded_date DESC"

    _description = "Biometric Data"

    recorded_date = fields.Datetime(index=True, default=lambda x: datetime.now())
    weight = fields.Float(string="Weight (kg)")
    height = fields.Float(string="Height (cm)")
    bmi = fields.Float(string="BMI (kg/m^2)")
    muac = fields.Float(string="MUAC (cm)")
