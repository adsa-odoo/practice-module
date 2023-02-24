from odoo import models,fields

class TripCarTag(models.Model):
    _name = "trip.car.tag"
    _description = "A Model for car tags"

    name = fields.Char(required = True,copy = False)
    color = fields.Integer(default = 2)

    _sql_constraints = [("_check_name","UNIQUE(name)","Tag name must be unique!")]