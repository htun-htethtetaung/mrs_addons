from odoo import fields, models


class ProfessionBackground(models.Model):
    _name = "partner.professional"

    _inherit = "partner.academic"

    name = fields.Char(string="Company Name or Hospital Name")
