import importlib
from datetime import timedelta, datetime
from odoo import fields, models, api

"""Refreshing a source's summary is defined as the process of :
- retrieving multiple pieces of information from the Google API that is represented by the source
- sending them to OpenAI API to generate a summary 
- storing the summary in the source's summary field."""


class Source(models.Model):
    """A source of information (a Google API representation on our end). Stores the user's data related to that source.
    Not to be confused with the module google_apis, which is the interface used to communicate with Google APIs."""

    _name = "proyecto_dam.source"

    display_name = fields.Char()  # Title Case, e.g. Google Maps
    name = fields.Char()  # snake_case, e.g. google_maps. Modules inside google_apis and images are named after it.
    summary = fields.Text()
    last_refresh = fields.Datetime(default=fields.Datetime.now())  # Last update of the summary

    # Specific to Google Oauth2.0 APIs
    refresh_token = fields.Char()
    scope = fields.Char()

    place_id = fields.Char()  # Specific to Google Places API

    def refresh_summary(self):
        """Refreshes the ``Source``'s ``summary`` if it's older than 1 hour."""

        for source in self:  # Extract the source from the recordset
            # if fields.Datetime.now() - self.last_refresh < timedelta(hours=1):

            # Sources are connected when they have a refresh_token (Google Oauth2.0 APIs) or a place_id (Google Places API)
            if source.refresh_token or source.place_id:
                module = importlib.import_module(f"odoo.addons.proyecto_dam.google_apis.{source.name}")
                summary = module.refresh_summary(source)
                if summary:
                    source.summary = summary
                    source.last_refresh = fields.Datetime.now()
                    source.write({"summary": source.summary, "last_refresh": source.last_refresh})

    def write(self, values):
        # We update the summary whenever any field is updated, which usually happens when refresh_token or place_id are updated (i.e. changes in config that could change outcome).
        # We don't want to update the summary when the only field that changes is the summary itself, because that would cause an infinite loop.
        if any(field != "summary" for field in values.keys()):
            self.refresh()

        result = super(Source, self).write(values)
        return result

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        """Wrapper around search_read that refreshes the ``summary`` of each ``Source`` before returning results."""
        sources = self.search(domain or [], offset=offset, limit=limit, order=order)
        for source in sources:
            source.refresh_summary()
        results = sources.read(fields, **read_kwargs)
        return results

        # for source in sources:
        #     source.refresh()
        # results = super(Source, self).search_read(domain, fields, offset, limit, order, **read_kwargs)
        # return results
