from odoo import api, exceptions, fields, models
from odoo.exceptions import UserError


class Property(models.Model):
    _name = "estate.property"
    _description = "Property information for real estate"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Property Description", required=True)
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date Availability", required=True, copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=+3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", required=False, copy=False, readonly=True,
                                 compute="_compute_selling_price")
    bedrooms = fields.Integer(string="Bedrooms", default=2, required=True)
    living_area = fields.Integer(string="Living Area (sqm)", required=True)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", required=False)
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[('north', 'North'),
                                                     ('south', 'South'),
                                                     ('east', 'East'),
                                                     ('west', 'West')])
    state = fields.Selection(string="State",
                             selection=[('new', 'New'),
                                        ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'),
                                        ('sold', 'Sold'),
                                        ('canceled', 'Canceled')],
                             required=True,
                             copy=False,
                             default="new")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="")
    total_area = fields.Float(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", default=0, compute="_compute_best_offer")

# -------------------------------------------------------------------------
# COMPUTE METHODS
# -------------------------------------------------------------------------

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=None)

    # Need to figure out how to pull / set values from other models
    # a change made in the offer view needs to make the main property view change.
    @api.depends("offer_ids.status")
    def _compute_selling_price(self):
        for record in self:
            if record.offer_ids == 'accepted':
                record.selling_price = 222

# -------------------------------------------------------------------------
# ON CHANGE METHODS
# -------------------------------------------------------------------------

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

# -------------------------------------------------------------------------
# ACTIONS
# -------------------------------------------------------------------------

    def mark_property_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            else:
                record.state = 'sold'
        return True

    def cancel_property(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            else:
                record.state = 'canceled'
        return True
