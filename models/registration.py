from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'fleet.vehicle'

    registration_date = fields.Date(string='Registration Date')
