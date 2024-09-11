from odoo import fields, models


class ProfessionBackground(models.Model):
    _name = "partner.professional"

    _inherit = "partner.academic"

    _description = "Doctor or Customer's Profession"

    name = fields.Char(string="Company Name or Hospital Name")
