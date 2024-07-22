from odoo import models, fields


class Visit(models.Model):
    _inherit = "mrs.visit"

    program_ids = fields.One2many(
        comodel_name="mrs.visit.program", inverse_name="visit_id", tracking=True
    )
