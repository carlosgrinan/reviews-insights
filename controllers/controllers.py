# -*- coding: utf-8 -*-

import logging
import random
from odoo import http

logger = logging.getLogger(__name__)


class Source(http.Controller):
    @http.route(
        "/proyecto_dam/source",
        type="json",
        auth="user",
        methods=["LIST"],
    )
    def list_sources(self):
        sources = http.request.env["proyecto_dam.source"].search([])
        return sources.read(["name", "summary"])
