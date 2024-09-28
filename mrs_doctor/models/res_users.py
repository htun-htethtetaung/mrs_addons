from odoo import models


class User(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "mail.thread.main.attachment", "mail.activity.mixin"]
