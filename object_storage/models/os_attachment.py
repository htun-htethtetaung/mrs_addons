import base64
import urllib.parse

from odoo import models, fields, api
from odoo.tools import human_size
from odoo.tools.mimetypes import guess_mimetype
from ..utils.env import AWS_BUCKET_NAME
from ..utils.s3 import s3


class OsAttachmentType(models.Model):
    _name = "os.attachment.type"

    _description = "Object Storage Attachment Type"

    name = fields.Char()
    code = fields.Char(index=True)
    active = fields.Boolean(default=True)


class OsAttachment(models.Model):
    _name = "os.attachment"

    _description = "Object Store Attachment"

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if (
            "params" in self._context
            and "model" in self._context.get("params")
            and "res_model" not in res
            and "default_res_model" not in self._context
        ):
            res.update({"res_model": self._context["params"]["model"]})
        return res

    name = fields.Char()
    bucket_name = fields.Char(index=True)
    store_fname = fields.Char(index=True)
    data = fields.Binary(compute="_compute_data", inverse="_inverse_data")
    size = fields.Integer()
    mimetype = fields.Char("Mime Type", readonly=True)
    res_model = fields.Char(index=True)
    res_id = fields.Many2oneReference(
        index=True, model_field="res_model", readonly=True
    )
    type = fields.Many2one(
        string="Document Type", comodel_name="os.attachment.type", index=True
    )
    note = fields.Text()

    @api.depends("store_fname", "bucket_name", "size")
    @api.depends_context("bin_size")
    def _compute_data(self):
        if self._context.get("bin_size"):
            for record in self:
                record.data = human_size(record.size)
        else:
            for record in self:
                record.data = b""
                if record.store_fname and record.bucket_name:
                    os_response = s3.get_object(record.store_fname, record.bucket_name)
                    bin_data = os_response["Body"].read()
                    if bin_data:
                        record.data = base64.b64encode(bin_data)

    def _inverse_data(self):
        for record in self:
            bin_data = base64.b64decode(record.data if record.data else b"")
            record.mimetype = self._compute_mimetype(bin_data)
            record.size = len(bin_data)
            record.bucket_name = AWS_BUCKET_NAME
            record.store_fname = s3.put_object(
                data=bin_data,
                filename=record.name,
                bucket_name=AWS_BUCKET_NAME,
                content_type=record.mimetype,
                metadata={
                    "res_model": record.res_model if record.res_model else "",
                    "res_id": str(record.res_id if record.res_id else ""),
                },
            )
            self._add_to_gc(name=record.store_fname, bucket_name=record.bucket_name)

    def _compute_mimetype(self, data: bytes):
        mimetype = guess_mimetype(data)
        return mimetype if mimetype else "application/octet-stream"

    def _add_to_gc(self, name: str, bucket_name: str):
        gc_file = self.env["os.attachment.gc"].search(
            [("name", "=", name), ("bucket_name", "=", bucket_name)]
        )
        if not gc_file:
            self.env["os.attachment.gc"].create(
                {"name": name, "bucket_name": bucket_name}
            )

    def preview(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Document Preview",
            "target": "new",
            "res_model": self._name,
            "view_id": self.env.ref(
                "object_storage.view_os_attachment_preview_form"
            ).id,
            "view_mode": "form",
            "res_id": self.id,  # pylint: disable=no-member
            "flags": {"mode": "readonly"},
        }

    def download(self):
        filename = urllib.parse.quote(self.name)
        return {
            "type": "ir.actions.act_url",
            "url": (
                f"/web/binary/download_os_attachment/{filename}?"
                f"res_id={str(self.ids[0])}&store_fname={self.store_fname}&filename={filename}"
            ),
            "target": "new",
        }

    def unlink(self):
        for record in self:
            self._add_to_gc(name=record.store_fname, bucket_name=record.bucket_name)
        return super().unlink()
