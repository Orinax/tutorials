from odoo import fields, models

class Property(models.Model):
    _name = "estate.property.tag"
    _description = "A model to enable the usage of tags for properties"

    name = fields.Char(string="Name", required=True)