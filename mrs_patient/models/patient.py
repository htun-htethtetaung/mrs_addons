from odoo import fields, models, api


class InsuranceProvider(models.Model):
    _name = "insurance.provider"
    _description = "Insurance Provider"

    name = fields.Char(string="Name", required=True)


class MrsHabits(models.Model):
    _name = "mrs.habits"
    _description = "Habits"

    name = fields.Char(string="Name", required=True)


class PatientInsurance(models.Model):
    _name = "patient.insurance"
    _description = "Insurance"

    policy_number = fields.Char(string="Policy Number", required=True)
    patient_id = fields.Many2one(
        comodel_name="res.partner", string="Patient Name", required=True
    )
    provider_id = fields.Many2one(
        comodel_name="insurance.provider", string="Insurance Provider", required=True
    )


class MrsPatient(models.Model):

    _inherit = "res.partner"

    is_patient = fields.Boolean(default=False, index=True)

    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection(
        [
            ("MALE", "Male"),
            ("FEMALE", "Female"),
            ("OTHER", "Other"),
            ("UNKNOWN", "Unknown"),
        ]
    )
    patient_code = fields.Char(
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: "New",
        size=10,
    )
    occupation = fields.Char()
    disability = fields.Boolean()
    habit_ids = fields.Many2many(
        comodel_name="mrs.habits", string="Habits", relation="mrs_patient_habits_rel"
    )
    insurance_ids = fields.One2many(
        comodel_name="patient.insurance", inverse_name="patient_id"
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("patient_code", "New") == "New":
                vals["patient_code"] = (
                    self.env["ir.sequence"].next_by_code("mrs.patient") or "New"
                )
        return super().create(vals_list)
