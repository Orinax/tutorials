from odoo import api, fields, models


class Property(models.Model):
    _name = "estate.property.offer"
    _description = "A model that will help display all offers for a property"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'),
                                                          ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property Name", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", default=fields.Datetime.add(fields.Datetime.today(), days=+7))

# -------------------------------------------------------------------------
# COMPUTE METHODS
# -------------------------------------------------------------------------

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(fields.Datetime.today(), days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            updated_validity = record.date_deadline - fields.Date.today()
            record.validity = updated_validity.days

# -------------------------------------------------------------------------
# ON CHANGE METHODS
# -------------------------------------------------------------------------



# -------------------------------------------------------------------------
# ACTIONS
# -------------------------------------------------------------------------

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True