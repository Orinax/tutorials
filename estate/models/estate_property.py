from odoo import fields, models

class Property(models.Model):
    _name = "estate.property"
    _description = "Property information for real estate"

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Property Description", required=True)
    postcode = fields.Char(string="Postcode", required=True)
    date_availability = fields.Date(string="Date Availability", required=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", required=True)
    bedrooms = fields.Integer(string="Bedrooms", required=True)
    living_area = fields.Integer(string="Living area", required=True)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", required=False)
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])