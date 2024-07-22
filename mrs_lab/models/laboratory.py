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

    _description = "Laboratory"

    visit_id = fields.Many2one(comodel_name="mrs.visit")
    patient_id = fields.Many2one(
        comodel_name="res.partner",
        related="visit_id.patient_id",
        store=True,
        readonly=False,
        index=True,
    )
    test_type_id = fields.Many2one(comodel_name="mrs.lab.test.type", string="Test Type")
    lab_ref_no = fields.Char(index=True)
    priority = fields.Selection(selection=list(LabPriority.name_value()))
    note = fields.Text()
