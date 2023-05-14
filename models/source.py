from odoo import models, fields, api


class Source(models.Model):
    _name = "proyecto_dam.source"
    name = fields.Char()
    img_name = fields.Char()
    summary = fields.Text()
    # token = fields.Char()
    # img_src = fields.Char()
