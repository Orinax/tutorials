from odoo import fields, models

class Property(models.Model):
    _name = "estate.property.offer"
    _description = "A model that will help display all offers for a property"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property Name", required=True)