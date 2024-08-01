from datetime import datetime
from odoo import fields, models

from .allergy_reaction import ReactionLevel


class AllergyLine(models.Model):
    _name = "mrs.allergy"

    _inherit = "mrs.visit.line.abstract"

    _order = "recorded_date desc"

    _description = "Visit Allergy Line"

    recorded_date = fields.Datetime(index=True, default=lambda x: datetime.now())
    allergen_id = fields.Many2one(comodel_name="mrs.allergen")
    other_allergen = fields.Boolean(
        related="allergen_id.other", string="Other Allergen"
    )
    allergen_detail = fields.Char()

    allergy_reaction_id = fields.Many2one(comodel_name="mrs.allergy.reaction")
    other_allergy_reaction = fields.Boolean(
        related="allergy_reaction_id.other", string="Other Allergy Reaction"
    )
    allergy_reaction_detail = fields.Char()

    reaction_level = fields.Selection(
        string="Severity of worst reaction", selection=list(ReactionLevel.name_value())
    )

    note = fields.Text()

    active = fields.Boolean(default=True)
