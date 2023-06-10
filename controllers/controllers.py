from odoo import http
from odoo.addons.reviews_insights.google_apis import api


class Source(http.Controller):
    @http.route(
        "/reviews_insights/connect",
        type="json",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def connect(self, **kwargs):
        id = http.request.params.get("id")
        config_id = http.request.params.get("config_id")

        # OAuth2.0 APIs
        code = http.request.params.get("code")
        if code:
            refresh_token = api.code_to_token(code)
        else:
            refresh_token = None

        # JS seems to turn null into false
        if config_id == False:
            config_id = None

        source = http.request.env["reviews_insights.source"].browse(id)
        result = source.write(
            {
                "refresh_token": refresh_token,
                "config_id": config_id,
                "connected": True,
                "generating_summary": True,
            }
        )
        source.with_delay().refresh_summary()

        return result
