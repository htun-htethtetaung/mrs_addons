from odoo import models, fields


class User(models.Model):
    _inherit: str = "res.users"

    default_mrs_location_id = fields.Many2one(comodel_name="mrs.location")
