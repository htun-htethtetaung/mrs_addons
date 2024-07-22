from odoo import fields, models


class VisitProgram(models.Model):
    _name = "mrs.visit.program"

    _inherit = "mrs.visit.line.abstract"

    _description = "MRS Program Enrollment"

    program_id = fields.Many2one(comodel_name="mrs.program")
    date_start = fields.Date()
    date_end = fields.Date()
    mrs_location_id = fields.Many2one(
        comodel_name="mrs.location", string="Enrollment Location"
    )
