from odoo import models,fields

class TripHotels(models.Model):
    _name = "trip.hotels"
    _description = "A model for hotels"

    name = fields.Char("Hotel name", required = True)
    location = fields.Char(required = True)
    ratings = fields.Selection(selection=[("0","0 star"),("1","1 star"),("2","2 star"),("3","3 star"),("4","4 star"),("5","5 star")],default="2")
    cost_per_room = fields.Float(required = True,default=1000)
    is_available = fields.Boolean("Availability",default = True)
    trip_ids = fields.One2many("trip.trip","hotel_id")

    _sql_constraints = [
        ("unique_name","unique(name)","Hotel name must be unique!"),
        ("check_cost","check(cost_per_room > 0)","Cost must be positive!")
    ]