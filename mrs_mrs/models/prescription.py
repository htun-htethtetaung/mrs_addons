from enum import Enum
from odoo import models, fields


class PrescriptionOrder(models.Model):
    _name = "mrs.prescription.order"

    _description = "Prescription Order"

    visit_id = fields.Many2one(comodel_name="mrs.visit")
    # Related to Dose
    is_dose_free_text = fields.Boolean("Free Text Dose?", default=False)
    dose_free_text = fields.Text()
    product_id = fields.Many2one(comodel_name="product.product", string="Drug")
    quantity = fields.Float(string="Dose")
    uom_id = fields.Many2one(comodel_name="uom.uom", string="Dose Unit")

    # Dose Frequency
    frequency_qty = fields.Float()
    frequency_uom_id = fields.Many2one(comodel_name="uom.uom")
    
    # Dose Duration
    start_date = fields.Datetime()
    duration = fields.Float()
    duration_uom_id = fields.Many2one(comodel_name="uom.uom")

    # Notes
    note = fields.Text()
    is_reason_needed = fields.Boolean()
    reason = fields.Text()

    # Dispensing
    dispensing_instruction = fields.Text()

class Laboratory(models.Model):
    _name = "mrs.lab"

    _description = "Laboratory"

    name = fields.Char(index=True)
    code = fields.Char()

class LabPriority(Enum):
    ROUTINE = "ROUTINE"
    STAT = "STAT"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)

class PrescriptionLab(models.Model):
    _name = "mrs.prescription.lab"

    _description = "Prescription Lab"

    visit_id = fields.Many2one(comodel_name="mrs.visit")
    laboratory_id = fields.Many2one(comodel_name="mrs.lab")
    lab_ref_no = fields.Char(index=True)
    priority = fields.Selection(selection=list(LabPriority.name_value()))
    instruction = fields.Text()
