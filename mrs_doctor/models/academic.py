from odoo import models, fields


class AcademicBackground(models.Model):
    _name = "partner.academic"

    _description = "Academic History"

    name = fields.Char("Academic Name")
    partner_id = fields.Many2one(comodel_name="res.partner", index=True, required=True)
    position = fields.Char("Speciality or Role")
    start = fields.Date()
    stop = fields.Date("Ended")
    current = fields.Boolean()
    detail = fields.Text()
