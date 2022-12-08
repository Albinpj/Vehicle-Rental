from odoo import api, fields, models
from datetime import date
from datetime import timedelta


class VehicleRequest(models.Model):
    _name = "vehicle.request"
    _description = "Vehicle Request"
    _rec_name = "sequence"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    customer_id = fields.Many2one("res.partner", string='Customer', required=True)
    request_date = fields.Date(string="Request Date", default=fields.date.today())
    vehicle_id = fields.Many2one('vehicle.rental', required=True, domain="[('state', '=', 'available')]")
    sequence = fields.Char(string="Sequence Number", readonly=True, required=True, copy=False, default='New')
    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    period = fields.Integer(string="Period", default='1')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.ref('base.INR'))
    rent_amount = fields.Monetary(compute='rent_amt', string="Rent Amount")
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm '), ('invoiced_to_request', 'Invoiced To Request'),
         ('returned', 'Returned')],
        default="draft", require=True,
        string="State")
    invoice_id = fields.Many2one('account.move')
    paid = fields.Boolean(compute='com_boolean', copy=False)
    period_type = fields.Selection([('hour', 'Hour'), ('day', 'Day'), ('week', 'Week'), ('month', 'Month')],
                                   string="Period Type")
    request_id = fields.Many2one('vehicle.rental', string='Request Id')

    def button_in_confirm(self):
        self.vehicle_id.state = 'not_available'
        self.write({
            'state': "confirm"
        })

    def button_in_returned(self):
        self.vehicle_id.state = 'available'
        self.write({
            'state': "returned"
        })

    @api.model
    def create(self, vals):
        if vals.get('sequence', 'New') == 'New':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('vehicle.request') or 'New'
        result = super(VehicleRequest, self).create(vals)
        return result

    @api.depends('period_type', 'vehicle_id', 'period')
    def rent_amt(self):
        for rec in self:
            if rec.vehicle_id and rec.period_type:
                for dec in rec.vehicle_id.rental_charges_ids:
                    if rec.period_type == dec.time:
                        rec.rent_amount = rec.period * dec.amount
            else:
                rec.rent_amount = False

    def action_create_invoice(self):
        self.state = 'invoiced_to_request'
        self.invoice_id = self.env['account.move'].create([
            {'move_type': 'out_invoice',
             'partner_id': self.customer_id,
             'ref': self.vehicle_id.name,
             'invoice_date': self.from_date,
             'invoice_line_ids': [(0, 0, {'name': self.vehicle_id.name,
                                          'price_unit': self.rent_amount})],
             }, ])
        return {
            'res_model': 'account.move',
            'res_id': self.invoice_id.id,
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
        }

    def action_view_invoice(self):
        return {
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'domain': [('ref', '=', self.vehicle_id.name)],
        }

    @api.depends('invoice_id.payment_state')
    def com_boolean(self):
        if self.invoice_id.payment_state == 'paid':
            self.paid = True
        else:
            self.paid = False

    @api.onchange('to_date')
    def warning_late(self):
        today = date.today()
        yesterday = today + timedelta(days=2)
        after_day = today - timedelta(days=1)
        if self.to_date == yesterday:
            self.vehicle_id.warning = True
        else:
            self.vehicle_id.warning = False
        if self.to_date == after_day:
            self.vehicle_id.late = True
        else:
            self.vehicle_id.late = False
