from odoo import fields, models

class Property(models.Model):
    _name = "estate.property"
    _description = "Property information for real estate"

    active = fields.Boolean(default=True)
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Property Description", required=True)
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date Availability", required=True, copy=False, default=fields.Datetime.add(fields.Datetime.today(), months=+3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", required=False, copy=False, readonly=True)
    bedrooms = fields.Integer(string="Bedrooms", default=2, required=True)
    living_area = fields.Integer(string="Living Area (sqm)", required=True)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", required=False)
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden area")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    state = fields.Selection(string="State", selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
                             required=True,
                             copy=False,
                             default="new")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
