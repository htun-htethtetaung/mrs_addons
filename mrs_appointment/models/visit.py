from odoo import fields, models


class Visit(models.Model):
    _inherit = "mrs.visit"

    calendar_event_id = fields.Many2one(comodel_name="calendar.event", index=True)
