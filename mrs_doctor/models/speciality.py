from odoo import fields, models


class Speciality(models.Model):
    _name = "mrs.doctor.speciality"

    name = fields.Char(index=True)
