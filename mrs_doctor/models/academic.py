from odoo import models, fields


class AcademicBackground(models.Model):
    _name = "partner.academic"

    name = fields.Char("Academic Name")
    position = fields.Char("Speciality or Role")
    start = fields.Date()
    stop = fields.Date("Ended")
    current = fields.Boolean()
    detail = fields.Text()
