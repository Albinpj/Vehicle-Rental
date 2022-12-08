from odoo import api, fields, models


class VehicleRental(models.Model):
    _name = "vehicle.rental"
    _description = "Vehicle rental"

    name = fields.Char(compute='comp_name', store=True)
    brand = fields.Char(string="Brand", related="vehicle_id.model_id.name", readonly=False)
    image = fields.Binary(string='Rental image')
    model_year = fields.Char(string='Model Year')
    registration_date = fields.Date(string=' Registration Date', related="vehicle_id.registration_date", readonly=False)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.INR'))
    state = fields.Selection([('available', 'Available'), ('not_available', 'Not Available'), ('sold', 'Sold')],
                             default="available",
                             string="State")
    vehicle_id = fields.Many2one('fleet.vehicle', required=True)
    warning = fields.Boolean(string='Warning', readonly=True)
    late = fields.Boolean(string='Late', readonly=True)
    rental_charges_ids = fields.One2many('rental.charges', 'charge_id', string='Rental Charges')
    rental_request_ids = fields.One2many('vehicle.request', 'request_id', string='Rental Request',
                                         compute='depends_rental_request')

    @api.depends('vehicle_id', 'model_year')
    def comp_name(self):
        year = str(fields.Date.to_date(self.registration_date))
        self.model_year = year[:4] if year != 'None' else False
        self.name = (self.vehicle_id.name or '') + (self.model_year or '')

    def vehicle_request(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Vehicles Request',
            'view_mode': 'tree,form',
            'res_model': 'vehicle.request',
            'domain': [('vehicle_id', '=', self.name)],
            'context': "{'create': True}"
        }

    @api.depends('vehicle_id')
    def depends_rental_request(self):
        for rec in self:
            rec.rental_request_ids = rec.rental_request_ids.search([('vehicle_id', '=', rec.id),
                                                                    ('state', '=', 'confirm')])
