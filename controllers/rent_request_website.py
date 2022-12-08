from odoo import http
from odoo.http import request


class WebsiteForm(http.Controller):

    @http.route(['/rent_request'], type='http', auth="user", website=True)
    def rent_request(self):
        partners = request.env['res.partner'].sudo().search([])
        vehicles = request.env['vehicle.rental'].sudo().search([('state', '=', 'available')])
        values = {'partners': partners, 'vehicles': vehicles}
        return request.render("vechile_rental.online_rent_request_form", values)

    @http.route(['/rent_request/submit'], type='http', auth="public", website=True)
    def rent_request_form_submit(self, **post):
        rent_request = request.env['vehicle.request'].sudo().create({
            'customer_id': post.get('partner_id'),
            'vehicle_id': post.get('vehicle_id'),
            'period_type': post.get('period_type'),
            'from_date': post.get('from_date'),
            'to_date': post.get('to_date'),
            'request_date': post.get('request_date'),
            'period': post.get('period'),
            'rent_amount': post.get('rent_amount'),

        })
        vals = {
            'rent_request': rent_request,
        }
        return request.render("vechile_rental.tmp_rent_request_form_success", vals)

    @http.route(['/create/customer'], type='http', auth="public", website=True)
    def partner_form(self, **post):
        return request.render("vechile_rental.tmp_customer_form", {})

    @http.route(['/customer/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone')
        })
        vals = {
            'partner': partner,
        }
        return request.render("vechile_rental.tmp_customer_form_success", vals)
