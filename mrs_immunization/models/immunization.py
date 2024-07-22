from odoo import fields, models


class Immunization(models.Model):
    _name = "mrs.immunization"

    _description = "MRS Immunization Master Data"

    name = fields.Char(required=True, index=True)
    code = fields.Char(required=True, index=True)
    product_id = fields.Many2one(comodel_name="product.product", required=True)
