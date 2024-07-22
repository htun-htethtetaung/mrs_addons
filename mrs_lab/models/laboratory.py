from enum import Enum
from odoo import models, fields


class LabPriority(Enum):
    ROUTINE = "ROUTINE"
    STAT = "STAT"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)


class PrescriptionLab(models.Model):
    _name = "mrs.lab"

    _inherit = "mrs.visit.line.abstract"

    _description = "Laboratory"

    test_type_id = fields.Many2one(comodel_name="mrs.lab.test.type", string="Test Type")
    lab_ref_no = fields.Char(index=True)
    priority = fields.Selection(selection=list(LabPriority.name_value()))
    note = fields.Text()
