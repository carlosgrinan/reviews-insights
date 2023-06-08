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
        id = http.request.params.get("id")
        config_id = http.request.params.get("config_id")

        refresh_token = api.code_to_token(code)

        # JS seems to turn null into false
        if config_id == False:
            config_id = None

        source = http.request.env["reviews_insights.source"].browse(id)
        source.write(
            {
                "refresh_token": refresh_token,
                "config_id": config_id,
                "connected": True,
            }
        )
