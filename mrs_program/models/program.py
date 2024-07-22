from odoo import fields, models


class Program(models.Model):
    _name = "mrs.program"

    _description = "MRS Program Master Data"

    name = fields.Char(required=True, index=True)
    code = fields.Char(required=True, index=True)
