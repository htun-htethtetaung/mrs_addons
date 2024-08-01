from odoo import models, fields


class OsAttachmentHolder(models.AbstractModel):
    _name = "os.attachment.holder"

    _description = "Object Storage Holder"

    def _default_res_model(self):
        return self._name

    res_model = fields.Char(default=_default_res_model)
    os_attachment_ids = fields.One2many(
        comodel_name="os.attachment",
        inverse_name="res_id",
        auto_join=True,
    )
