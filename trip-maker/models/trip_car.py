from odoo import models,fields

class TripCar(models.Model):
    _name = "trip.car"
    _description = "Car model"

    name = fields.Char("Car name")
    capacity = fields.Integer(default = 4)
    cost_per_km = fields.Float("Cost per km")
    is_available = fields.Boolean(default = True)