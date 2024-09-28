from odoo import models, fields


class MrsLocation(models.Model):
    _name: str = "mrs.location"

    _description: str = "Clinic Location"

    name = fields.Char()
    code = fields.Char()
    address = fields.Text()


class Doctor(models.Model):
    _inherit = "res.partner"

    default_mrs_location_id = fields.Many2one(comodel_name="mrs.location")
