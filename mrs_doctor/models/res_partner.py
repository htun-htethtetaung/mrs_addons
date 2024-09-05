from odoo import models, fields


class Doctor(models.Model):
    _inherit = "res.partner"

    languages = fields.Many2many(comodel_name="res.lang")

    reg_country = fields.Many2one(
        comodel_name="res.country", string="Countries of Registration"
    )
    speciality_ids = fields.Many2one(comodel_name="res.doctor.specility", index=True)
