from odoo import models,fields,api
from dateutil.relativedelta import relativedelta

class TripTrip(models.Model):
    _name = "trip.trip"
    _description = "Trip model"

    name = fields.Char(compute = "_compute_name")
    origin = fields.Char(default = "Ahmedabad",required = True)
    destination = fields.Char(required = True)
    schedule = fields.Date(required = True)
    distance = fields.Float("Distance (km)",required = True)
    members = fields.Integer("Total members")
    car_ids = fields.One2many("trip.car","trip_id",required = True)
    cost = fields.Float("Cost (Rs.)",compute = "_compute_cost")
    status = fields.Selection(selection = [('pending','Pending'),('progress','In Progress'),('done','Done')])

    @api.depends("origin","destination")

    def _compute_name(self):
        for record in self:
            if(record.origin and record.destination):
                record.name = "%s - %s" %(record.origin,record.destination)
            else:
                record.name = ""
    @api.depends("car_ids.cost_per_km")

    def _compute_cost(self):
        for outer_record in self:
            outer_record.cost = 0
            for inner_record in outer_record.car_ids:
                outer_record.cost += inner_record.cost_per_km * outer_record.distance
    def action_pending(self):
        for record in self:
            record.status = "pending"
        return True
    
    def action_progress(self):
        for record in self:
            record.status = "progress"
        return True

    def action_done(self):
        for record in self:
            record.status = "done"
        return True
    