from odoo import models, fields


class Doctor(models.Model):
    _inherit = "res.partner"

    languages = fields.Many2many(comodel_name="res.lang")

    reg_country = fields.Many2one(
        comodel_name="res.country", string="Countries of Registration"
    )
    speciality_ids = fields.Many2one(comodel_name="res.doctor.specility", index=True)
    sub_speciality = fields.Text(string="Sub-Specialities")
    expretise = fields.Text(string="Area of Expertise")
    academic_ids = fields.One2many(
        comodel_name="partner.academic", inverse_name="partner_id"
    )
    professional_ids = fields.One2many(
        comodel_name="partner.professional", inverse_name="partner_id"
    )
    default_mrs_location_id = fields.Many2one(comodel_name="mrs.location")
