from odoo import models, fields


class Diagnosis(models.Model):
    _name = "mrs.diagnosis"

    _description = "Diagnosis Master Data"

    name = fields.Char()
    code = fields.Char()

    note = fields.Text()
