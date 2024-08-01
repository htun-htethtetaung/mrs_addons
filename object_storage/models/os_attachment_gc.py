from odoo import models, fields


class OsAttachmentGc(models.Model):
    _name = "os.attachment.gc"

    _description = "Object Storage Attachemt Garbage Collector"

    name = fields.Char(index=True)
    bucket_name = fields.Char(index=True)
