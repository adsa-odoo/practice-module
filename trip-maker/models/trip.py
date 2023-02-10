from odoo import models,fields

class Trip(models.Model):
    _name = "trip"
    _description = "Trip model"

    name = fields.Char()
    origin = fields.Char(default = "Ahmedabad")
    destination = fields.Char()
    schedule = fields.Date()
    distance = fields.Float("Distance (km)")
    members = fields.Integer("Total members")
    