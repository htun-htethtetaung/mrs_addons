from enum import Enum
from datetime import datetime
from odoo import fields, models


class DiagnosisConditionStatus(Enum):
    PRIMARY = "Primary"
    SECONDARY = "Secondary"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)


class DiagnosisCondition(models.Model):
    _name = "mrs.diagnosis.condition"

    _inherit = ["mrs.visit.line.abstract", "os.attachment.holder"]

    _order = "start_date desc"

    _description = "Diagnosis Conditions"

    diagnosis_id = fields.Many2one(comodel_name="mrs.diagnosis")
    state = fields.Selection(
        selection=list(DiagnosisConditionStatus.name_value()),
        default=DiagnosisConditionStatus.PRIMARY.name,
    )
    start_date = fields.Datetime(index=True, default=lambda x: datetime.now())
    end_date = fields.Datetime()
    note = fields.Text()
    active = fields.Boolean(default=True, index=True)
