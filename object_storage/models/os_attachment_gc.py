# pylint: disable=broad-exception-caught
import logging
from odoo import models, fields
from ..utils.s3 import s3

_logger = logging.getLogger("#os_gc")


class OsAttachmentGc(models.Model):
    _name = "os.attachment.gc"

    _description = "Object Storage Attachemt Garbage Collector"

    name = fields.Char(index=True)
    bucket_name = fields.Char(index=True)

    def schedule_gc(self, limit: int = 100):
        _logger.info("Object Storage GC started")
        for record in self.search([], limit=limit):
            try:
                if not self.env["os.attachment"].search_count(
                    [("store_fname", "=", record.name)]
                ):
                    _logger.info("Deleted file [%s]", record.name)
                    s3.delete_object(record.name, record.bucket_name)
                record.unlink()
                self._cr.commit()
            except Exception:
                _logger.exception("Error on gc")
        _logger.info("Object Storage GC ended")
