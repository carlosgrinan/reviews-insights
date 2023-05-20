import importlib
from datetime import timedelta, datetime
from odoo import fields, models, api


class Source(models.Model):
    _name = "proyecto_dam.source"
    display_name = fields.Char()
    name = fields.Char()
    summary = fields.Text()
    # Specific to Google Oauth2.0 APIs
    refresh_token = fields.Char()
    scope = fields.Char()

    place_id = fields.Char()  # Specific to Google Places API
    last_sync = fields.Datetime(default=fields.Datetime.now())

    def sync(self):
        """Refreshes the summary if it's older than 1 hour."""
        for source in self:
            # if fields.Datetime.now() - self.last_sync < timedelta(hours=1):
            module = importlib.import_module(f"odoo.addons.proyecto_dam.google_apis.{source.name}")
            summary = module.sync(source)
            if summary:
                source.summary = summary
                source.last_sync = fields.Datetime.now()
                source.write({"summary": source.summary, "last_sync": source.last_sync})

    def write(self, values):
        # We update the summary whenever any field is updated, which happens when refresh_token... are updated (i.e. changes in config thtat could change outcome).
        # We don't want to update the summary when the only field that changes is the summary itself, because that would cause an infinite loop.
        if any(field != "summary" for field in values.keys()):
            self.sync()

        res = super(Source, self).write(values)
        return res

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **read_kwargs):
        """Wrapper around search_read that syncs summaries before returning results."""
        sources = self.search([])
        for source in sources:
            source.sync()

        results = super(Source, self).search_read(domain, fields, offset, limit, order, **read_kwargs)
        return results

    # @api.model
    # def sync_all(self):
    #     """Syncs summaries for all sources."""
    #     for source in self.search([]):
    #         source.sync()
