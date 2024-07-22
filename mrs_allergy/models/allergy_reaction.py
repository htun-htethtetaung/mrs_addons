from enum import Enum
from odoo import fields, models


class AllergenReaction(models.Model):
    _name = "mrs.allergy.reaction"

    name = fields.Char()
    other = fields.Boolean(default=False, readonly=True)


class ReactionLevel(Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)
