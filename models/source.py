from odoo import models, fields
import importlib


class Source(models.Model):
    _name = "proyecto_dam.source"
    name = fields.Char()
    img_name = fields.Char()  # TODO: change to name, and change name to display_name
    summary = fields.Text()
    refresh_token = fields.Char()

    def sync(self):
        module = importlib.import_module(self.name)
        module.sync()
