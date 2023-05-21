from odoo import http
from google_apis.api import code_to_token


class Source(http.Controller):
    @http.route(
        "/proyecto_dam/oauth2",
        type="json",
        auth="user",
    )
    def code_to_token(self):
        code = http.request.params.get("code")
        refresh_token = code_to_token(code)
        id = http.request.params.get("id")
        source = http.request.env["proyecto_dam.source"].browse(id)
        source.write({"refresh_token": refresh_token})
