import importlib
from datetime import datetime, timedelta, timezone
import time

from odoo import api, fields, models
from odoo.addons.bus.websocket import Websocket
from ..openai_api import openai_api

"""Refreshing a source's summary is defined as the process of :
- retrieving multiple pieces of information from the Google API that is represented by the source
- sending them to OpenAI API to generate a summary 
- storing the summary in the source's summary field."""


class Source(models.Model):
    """A source of information (a Google API representation on our end). Stores the user's data related to that source.
    Not to be confused with the module google_apis, which is the interface used to communicate with Google APIs."""

    _name = "reviews_insights.source"

    display_name = fields.Char()  # Title Case, e.g. Google Maps
    name = fields.Char()  # snake_case, e.g. google_maps. Modules inside google_apis and images are named after it.
    summary = fields.Text()
    last_refresh = fields.Datetime()  # Last update of the summary

    # Specific to Google Oauth2.0 APIs
    refresh_token = fields.Char()
    scope = fields.Char()

    config_id = fields.Char()
    config_placeholder = fields.Char()

    def needs_refresh(self):
        """Returns True if the summary needs to be refreshed."""
        if not self.summary:
            needs_refresh = True
        else:
            needs_refresh = datetime.now(timezone.utc) - self.last_refresh.replace(tzinfo=timezone.utc) > timedelta(hours=1)

        # Sources are connected when they have a refresh_token (Google Oauth2.0 APIs) and/or a config_id
        connected = self.refresh_token or self.config_id

        return connected and needs_refresh

    def refresh_summary(self):
        module = importlib.import_module(f"odoo.addons.reviews_insights.google_apis.{self.name}")
        summary = module.refresh_summary(self)
        if not summary:
            summary = _("No hay suficientes datos para generar un resumen. Por favor, conecta otra cuenta.")

        summary = self.translate_summary(summary)

        self.write({"summary": summary, "last_refresh": fields.Datetime.now()})

    @api.model
    def translate_summary(self, summary):
        """Translates the summary to the user's language."""
        lang_code = self.env.user.lang

        if lang_code:
            lang = self.env["res.lang"].search([("code", "=", lang_code)], limit=1)
            if lang:
                lang_name = lang.name
        else:
            lang_name = "English"

        summary = openai_api.translate(summary, lang_name)

        return summary

    def write(self, values):
        """Wrapper around write that calls ``refresh_summary()`` on each ``Source`` involved when the source has connected (refresh_token or config_id have changed)."""

        # Write and then re-browse so that refresh_summary() uses the updated records (e.g. a new refresh token)
        result = super().write(values)
        if not any(field == "summary" for field in values.keys()):
            self = self.browse(self.ids)
            for source in self:
                if source.needs_refresh():
                    source.with_delay().refresh_summary()

            # Placeholder summary
            self.write({"summary": "Generating summary...", "last_refresh": fields.Datetime.now()})

        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        """Wrapper around search_read that refreshes the ``summary`` of each ``Source`` before returning results."""

        sources = self.search(domain or [], offset=offset, limit=limit, order=order)
        for source in sources:
            source.refresh_summary()
        results = sources.read(fields, **read_kwargs)
        return results
