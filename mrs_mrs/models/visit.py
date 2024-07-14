from datetime import datetime
from odoo import fields, models

class Visit(models.Model):
    _name = "mrs.visit"

    _description = "Visit to patient"

    _inherits = {
        
    }
    _inherit = ['mail.thread.main.attachment', 'mail.activity.mixin']

    patient_id = fields.Many2one(comodel_name="res.partner")
    doctor_id = fields.Many2one(comodel_name="res.users")
    start_date = fields.Datetime(default=lambda x:datetime.now(), index=True)
    end_date = fields.Datetime(readonly=True)

    # Prescription
    prescription_order_ids = fields.One2many(comodel_name="mrs.prescription.order", inverse_name="visit_id")
    prescription_lab_ids = fields.One2many(comodel_name="mrs.prescription.lab", inverse_name="visit_id")
