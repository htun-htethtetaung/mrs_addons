from odoo import fields, models


class Speciality(models.Model):
    _name = "mrs.doctor.speciality"

    _description = "Doctor's Spciality"

    name = fields.Char(index=True)
