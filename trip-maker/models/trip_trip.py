from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta


class TripTrip(models.Model):
    _name = "trip.trip"
    _description = "Trip model"

    name = fields.Char(compute="_compute_name")
    origin = fields.Char(default="Ahmedabad", required=True)
    destination = fields.Char(required=True)
    schedule = fields.Date(required=True)
    distance = fields.Float("Distance (km)", required=True)
    members = fields.Integer("Total members")
    car_ids = fields.Many2many("trip.car", required=True)
    cost = fields.Float("Cost (Rs.)", compute="_compute_cost")
    state = fields.Selection(selection=[('pending', 'Pending'), ('progress', 'In Progress'), (
        'done', 'Done'), ('cancel', 'Cancel')], default="pending", readonly=True)
    hotel_id = fields.Many2one("trip.hotels", string="Hotel")
    halt = fields.Integer(string="Halt (Days)", default=1)

    @api.depends("origin", "destination")
    def _compute_name(self):
        for record in self:
            if (record.origin and record.destination):
                record.name = "%s - %s" % (record.origin, record.destination)
            else:
                record.name = ""

    @api.depends("car_ids.cost_per_km", "hotel_id.cost_per_room")
    def _compute_cost(self):
        for outer_record in self:
            outer_record.cost = 0
            for inner_record in outer_record.car_ids:
                outer_record.cost += inner_record.cost_per_km * outer_record.distance
                inner_record.is_available = False
            outer_record.cost += self.hotel_id.cost_per_room * outer_record.halt


    def action_pending(self):
        for record in self:
            if (record.state == "progress" or record.state == "done"):
                raise exceptions.UserError("Invalid action!")
            elif (record.state == "cancel"):
                raise exceptions.UserError("Trip is canceled!")
            else:
                record.state = "pending"
        return True

    def action_progress(self):
        for record in self:
            if (record.state == "done"):
                raise exceptions.UserError("Invalid action!")
            elif (record.state == "cancel"):
                raise exceptions.UserError("Trip is canceled!")
            else:
                record.state = "progress"
        return True

    def action_done(self):
        for record in self:
            if (record.state == "cancel"):
                raise exceptions.UserError("Trip is canceled!")
            else:
                record.state = "done"
        return True

    def action_cancel(self):
        for record in self:
            if (record.state == "progress"):
                raise exceptions.UserError(
                    "Trip is in progress, can't be canceled!")
            elif (record.state == "done"):
                raise exceptions.UserError("Trip is done, can't be canceled!")
            else:
                record.state = "cancel"
        return True

    @api.constrains("destination")
    def check_destination(self):
        for record in self:
            if (record.origin.lower() == record.destination.lower()):
                raise exceptions.ValidationError(
                    "Destination can't be same as origin")

    @api.constrains("distance")
    def check_distance(self):
        for record in self:
            if (record.distance <= 0):
                raise exceptions.ValidationError("Distance must be positive!")

    @api.constrains("car_ids")
    def check_car_ids(self):
        for record in self:
            if (not record.car_ids):
                raise exceptions.ValidationError(
                    "At least one car must be selected!")

    @api.constrains("members")
    def check_members(self):
        for record in self:
            if (record.members <= 0):
                raise exceptions.ValidationError(
                    "Number of members must be positive!")
