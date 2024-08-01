from odoo import fields, models


class VisitProgram(models.Model):
    _name = "mrs.visit.immunization"

    _inherit = "mrs.visit.line.abstract"

    _order = "expire_date"

    _description = "MRS Immunization Enrollment"

    immunization_id = fields.Many2one(comodel_name="mrs.immunization")
    dose_number = fields.Integer(string="Dose Number Within Series")
    manufacturer = fields.Char()
    vaccination_date = fields.Datetime()
    expire_date = fields.Datetime(index=True)
    note = fields.Text()
