from odoo import models,fields

class Trip(models.Model):
    _name = "trip"
    _description = "Trip model"

    name = fields.Char()
    origin = fields.Char()
    destination = fields.Char()
    schedule = fields.Date()
    distance = fields.Float()
