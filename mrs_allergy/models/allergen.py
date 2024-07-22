from enum import Enum
from odoo import fields, models


class AllergenType(Enum):
    AIRBORNE = "Airborne"
    FOOD = "Food"
    MEDICATION = "Medication"
    SKIN = "Skin"
    OTHER = "Other"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)


class Allergen(models.Model):
    _name = "mrs.allergen"

    _description = "Allergen"

    name = fields.Char()
    type = fields.Selection(
        selection=list(AllergenType.name_value()), default=AllergenType.FOOD
    )
    other = fields.Boolean(default=False, readonly=True)
