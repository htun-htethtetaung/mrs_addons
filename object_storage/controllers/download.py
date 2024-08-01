# -*- coding: utf-8 -*-
import base64
import urllib.parse

from odoo import http
from odoo.http import request, Controller


class DownloadController(Controller):
    @staticmethod
    def calculate_output(filecontent: bytes | None, filename: str | None):
        if filecontent:
            if not filename:
                filename = "download"
            output = request.make_response(
                filecontent,
                {
                    "Content-Type": "application/octet-stream",
                    "Content-Disposition": urllib.parse.quote(filename),
                },
            )
        else:
            output = request.not_found()
        return output

    @http.route(
        "/web/binary/download_os_attachment/<string:filename>", type="http", auth="user"
    )
    def download_document(self, **kw):
        res_id = kw.get("res_id")
        model = request.env["os.attachment"]
        store_fname = kw.get("store_fname")
        attachment = model.browse([int(res_id)])
        filecontent = None
        if attachment.store_fname == store_fname:
            filecontent = base64.b64decode(attachment.data)
        return self.calculate_output(filecontent=filecontent, filename=attachment.name)
