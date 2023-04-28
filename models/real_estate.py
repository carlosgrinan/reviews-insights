from odoo import models, fields


class RealEstate(models.Model):
    _name = "real.estate"

    name = fields.Char()