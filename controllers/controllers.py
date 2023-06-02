from odoo import http
from odoo.addons.reviews_insights.google_apis import api


class Source(http.Controller):
    @http.route(
        "/reviews_insights/oauth2",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def code_to_token(self, **kwargs):
        code = http.request.params.get("code")
        refresh_token = api.code_to_token(code)
        id = http.request.params.get("id")
        source = http.request.env["reviews_insights.source"].browse(id)
        source.write({"refresh_token": refresh_token})
