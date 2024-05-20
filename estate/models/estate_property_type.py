from odoo import fields, models

class Property(models.Model):
    _name = "estate.property.type"
    _description = "A model to highlight different types of properties"

    name = fields.Char(string="Property Type", required=True)
