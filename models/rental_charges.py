from odoo import api, fields, models


class RentalCharges(models.Model):
    _name = "rental.charges"
    _description = " Rental Charges"

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.INR'))
    time = fields.Selection(selection=[('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'), ('month', 'Month')],
                            string="Time")
    amount = fields.Monetary(string='Amount')
    charge_id = fields.Many2one('vehicle.rental', string='Charge Id')
