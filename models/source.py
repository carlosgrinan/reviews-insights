import importlib
from datetime import datetime, timedelta, timezone
import time

from odoo import api, fields, models
from odoo.addons.bus.websocket import Websocket
from ..openai_api import openai_api

"""Refreshing a source's summary is defined as the process of :
- retrieving multiple pieces of information from the Google API that is represented by the source
- sending them to OpenAI API to generate a summary 
- storing the summary in the source's summary field.

"""


class Source(models.Model):
    """A source of information (a Google API representation on our end). Stores the user's data related to that source.
    Not to be confused with the module google_apis, which is the interface used to communicate with Google APIs."""

    _name = "reviews_insights.source"

    display_name = fields.Char()  # Title Case, e.g. Google Maps
    name = fields.Char()  # snake_case, e.g. google_maps. Modules inside google_apis and images are named after it.
    summary = fields.Text()
    last_refresh = fields.Datetime()  # Last update of the summary
    generating_summary = fields.Boolean(default=False)

    connected = fields.Boolean(default=False)

    # Specific to Google Oauth2.0 APIs
    refresh_token = fields.Char()
    scope = fields.Char()

    # Null on Gmail and Business Profile
    config_id = fields.Char()
    config_placeholder = fields.Char()

    def write(self, values):
        """Wrapper around write that calls ``refresh_summary()`` on each ``Source`` involved when the source has connected."""

        # Write and then re-browse so that refresh_summary() uses the updated records (e.g. a new refresh token)
        result = super().write(values)
        if not any(field == "summary" for field in values.keys()):
            self = self.browse(self.ids)
            for source in self:
                if source.needs_refresh():
                    self.write({"generating_summary": True})
                    source.with_delay().refresh_summary()

        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        """Wrapper around search_read that refreshes the ``summary``"""

        sources = self.search(domain or [], offset=offset, limit=limit, order=order)

        if sources.__len__() == 1:
            source = sources[0]
            if source.needs_refresh():
                super().write({"generating_summary": True})
                source.with_delay().refresh_summary()

        results = sources.read(fields, **read_kwargs)
        return results

    def needs_refresh(self):
        """Returns True if the summary needs to be refreshed."""
        if not self.summary:
            needs_refresh = True
        else:
            needs_refresh = datetime.now(timezone.utc) - self.last_refresh.replace(tzinfo=timezone.utc) > timedelta(hours=1)

        return self.connected and needs_refresh and not self.generating_summary

    def refresh_summary(self):
        """Updates the ``summary`` field with a new summary or an error message"""

        module = importlib.import_module(f"odoo.addons.reviews_insights.google_apis.{self.name}")
        summary = module.refresh_summary(self)
        if not summary:
            summary = _("No hay suficientes datos para generar un resumen. Por favor, conecta otra cuenta.")

        summary = self.translate_summary(summary)

        self.write({"summary": summary, "last_refresh": fields.Datetime.now(), "generating_summary": False})

    @api.model
    def translate_summary(self, summary):
        """Returns the ``summary`` translated to the user's language, or an error message"""

        lang_code = self.env.user.lang
        if lang_code:  # user might not have a language set, which Odoo defaults to English
            if not "en" in lang_code:  # summary is already in English
                lang = self.env["res.lang"].search([("code", "=", lang_code)], limit=1)
                summary = openai_api.translate(summary, lang.name)

        return summary


# class IrHttp(models.AbstractModel):
#     _inherit = "ir.http"

#     @classmethod
#     def _get_translation_frontend_modules_name(cls):
#         modules = super()._get_translation_frontend_modules_name()
#         return modules + ["reviews_insights"]
