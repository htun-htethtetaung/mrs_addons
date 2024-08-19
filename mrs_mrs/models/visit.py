# pylint: disable=no-member
from datetime import datetime
from enum import Enum
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

IR_ACT_WINDOW = "ir.actions.act_window"


class VisitStatus(Enum):
    DRAFT = "Draft"
    START = "Started"
    ENDED = "Ended"

    @classmethod
    def name_value(cls):
        for item in cls:
            yield (item.name, item.value)


class Visit(models.Model):
    _name = "mrs.visit"

    _description = "Visit to patient"

    _order = "start_date DESC"

    _inherit = ["mail.thread.main.attachment", "mail.activity.mixin"]

    patient_id = fields.Many2one(
        index=True,
        comodel_name="res.partner",
        required=True,
        tracking=True,
        domain="[('is_patient', '=', True)]",
    )
    name = fields.Char(
        string="Visit ID",
        copy=False,
        required=True,
        readonly=True,
        size=13,
        index=True,
        default=lambda self: "New",
    )
    doctor_id = fields.Many2one(
        comodel_name="res.users", default=lambda x: x.env.user.id
    )
    state = fields.Selection(
        selection=list(VisitStatus.name_value()),
        index=True,
        default=VisitStatus.DRAFT.name,
        tracking=True,
    )
    is_external_doctor = fields.Boolean(default=False)
    external_doctor_name = fields.Char(size=30)
    start_date = fields.Datetime(
        default=lambda x: datetime.now(), index=True, tracking=True
    )
    backdate = fields.Boolean(default=False)
    end_date = fields.Datetime(readonly=True)
    mrs_location_id = fields.Many2one(comodel_name="mrs.location")

    note = fields.Text(tracking=True)

    @api.constrains("patient_id", "state")
    def _open_visit_per_patient(self):
        open_states = (VisitStatus.START.name, VisitStatus.DRAFT.name)
        for record in self:
            if (
                record.state in open_states
                and record.patient_id
                and self.search_count(
                    [
                        ("id", "!=", record.id),
                        ("patient_id", "=", record.patient_id.id),
                        ("state", "in", open_states),
                    ]
                )
            ):
                raise ValidationError(
                    _("Please end the previous (draft or started) visit!")
                )

    @api.onchange("doctor_id")
    def _onchange_doctor_id(self):
        for record in self:
            if record.doctor_id:
                record.mrs_location_id = record.doctor_id.default_mrs_location_id.id

    @api.onchange("is_external_doctor")
    def _onchange_is_external_doctor(self):
        for record in self:
            if record.is_external_doctor:
                record.doctor_id = None

    def action_start(self):
        for record in self:
            record.state = VisitStatus.START.name
            record.start_date = (
                record.start_date if record.start_date else datetime.now()
            )

    def action_end(self):
        for record in self:
            record.state = VisitStatus.ENDED.name
            record.end_date = record.end_date if record.end_date else datetime.now()

    def get_current_visit(self, patient_id: int):
        record = self.search(
            [
                ("patient_id", "=", patient_id),
                ("state", "in", (VisitStatus.START.name, VisitStatus.DRAFT.name)),
            ]
        )
        return record[0] if record else False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = (
                    self.env["ir.sequence"].next_by_code("mrs.visit") or "New"
                )
        return super().create(vals_list)

    def action_go_to_visit(self):
        self.ensure_one()
        action = {
            "type": IR_ACT_WINDOW,
            "view_type": "form",
            "res_model": "mrs.visit",
            "view_mode": "form",
            "context": self._context,
            "domain": [("id", "=", self.id)],
            "res_id": self.id,
        }
        return action
