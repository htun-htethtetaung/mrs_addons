from odoo import models, fields


class LabTestType(models.Model):
    _name = "mrs.lab.test.type"

    _description = "Test Type"

    name = fields.Char(index=True)
    code = fields.Char()
