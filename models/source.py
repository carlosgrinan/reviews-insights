import importlib
from datetime import datetime, timedelta, timezone
import time

from odoo import api, fields, models
from odoo.addons.bus.websocket import Websocket

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

    place_id = fields.Char()  # Specific to Google Places API

    def refresh_summary(self):
        """Refreshes the ``Source``'s ``summary`` if it's older than 1 hour."""
        self.ensure_one()

        if not self.last_refresh:
            needs_refresh = True
        else:
            needs_refresh = datetime.now(timezone.utc) - self.last_refresh.replace(tzinfo=timezone.utc) > timedelta(hours=1)

        # Sources are connected when they have a refresh_token (Google Oauth2.0 APIs) or a place_id (Google Places API)
        connected = self.refresh_token or self.place_id

        time.sleep(15)  # TODO QUITAR
        self.env["bus.bus"]._sendone("my-channel", "my-type", {"message_key": " a demo async message"})
        print("ASYNC JOB")
        # if connected and needs_refresh:
        # module = importlib.import_module(f"odoo.addons.proyecto_dam.google_apis.{self.name}") #TODO descomentar, es para no gastar cuota
        # summary = module.refresh_summary(self)
        # if summary:
        #     self.write({"summary": summary, "last_refresh": fields.Datetime.now()})

    def write(self, values):
        result = super().write(values)

        # We update the summary whenever summary is not updated, which usually happens when refresh_token or place_id are updated (i.e. changes in config that could change outcome).
        # We don't want to update the summary when summary changes, because that would cause an infinite loop.
        # if not any(field == "summary" for field in values.keys()):
        #     # Re-browse the records to get the updated values, so refresh_summary() uses, for example, the updated refresh_token.
        #     self = self.browse(self.ids)
        #     for source in self:
        #         print("WRITING")
        #         source.refresh_summary()

        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        """Wrapper around search_read that refreshes the ``summary`` of each ``Source`` before returning results."""

        # time.sleep(5)  # QUITAR
        sources = self.search(domain or [], offset=offset, limit=limit, order=order)
        # for source in sources:
        # source.refresh_summary()
        # source.with_delay().refresh_summary()
        self.env["bus.bus"]._sendone("my-channel", "my-type", {"message_key": " a demo message"})
        results = sources.read(fields, **read_kwargs)
        return results


@Websocket.onopen
def onopen(env, websocket):
    print("CONECTADO A WEBSOCKET")
    print(websocket)
    print(env)
