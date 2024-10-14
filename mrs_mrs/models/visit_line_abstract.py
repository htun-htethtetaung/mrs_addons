from odoo import models, fields
from .visit import VisitStatus


class VisitLine(models.AbstractModel):
    _name = "mrs.visit.line.abstract"

    _description = "Abstract Model For All Visit Lines"

    visit_id = fields.Many2one(comodel_name="mrs.visit", index=True)
    visit_state = fields.Selection(
        related="visit_id.state", selection=list(VisitStatus.name_value())
    )
    patient_id = fields.Many2one(
        comodel_name="res.partner",
        index=True,
        store=True,
        readonly=False,
        related="visit_id.patient_id",
    )
    active = fields.Boolean(default=True, index=True)
