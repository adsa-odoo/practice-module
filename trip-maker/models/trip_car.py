from odoo import models,fields,api,exceptions

class TripCar(models.Model):
    _name = "trip.car"
    _description = "Car model"

    name = fields.Char("Car name")
    capacity = fields.Integer(default = 4)
    cost_per_km = fields.Float("Cost per km")
    is_available = fields.Boolean(default = True)

    @api.constrains("cost_per_km")
    def check_cost_per_km(self):
        for record in self:
            if(record.cost_per_km <= 0):
                exceptions.ValidationError("Cost must be positive!")

    @api.constrains("capacity")
    def check_capacity(self):
        for record in self:
            if(record.capacity <= 0):
                exceptions.ValidationError("Capacity must be positive!")