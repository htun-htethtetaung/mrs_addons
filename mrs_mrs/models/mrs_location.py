from odoo import models, fields


class MrsLocation(models.Model):
    _name: str = "mrs.location"

    _description: str = "Clinic Location"

    name = fields.Char()
    code = fields.Char()
    address = fields.Text()
