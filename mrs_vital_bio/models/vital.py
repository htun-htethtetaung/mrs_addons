from datetime import datetime
from odoo import models, fields


class Vital(models.Model):
    _name = "mrs.vital"

    _inherit = "mrs.visit.line.abstract"

    _order = "recorded_date DESC"

    _description = "Vital Data"

    recorded_date = fields.Datetime(index=True, default=lambda x: datetime.now())
    temperature = fields.Float(string="TEMP (DEG C)")
    blood_pressure = fields.Float(string="B/P (mmHg)")
    pulse = fields.Float(string="Pulse (beats/min)")
    respiration_rate = fields.Float(string="R. Rate (B./min)")
    spo_two = fields.Float(string="SpO2 (%)")
