import json
from odoo import http
from odoo.http import content_disposition, request
from odoo.addons.web.controllers.main import _serialize_exception
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name, **kw):
        uid = request.session.uid
        report_obj = request.env[model].sudo(uid)
        print(report_obj)
        options = json.loads(options)
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[('Content-Type', 'application/vnd.ms-excel'),
                             ('Content-Disposition', content_disposition(report_name + '.xlsx'))
                             ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', 'dummy token')
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))


# Rent amount calculation

class period(http.Controller):
    @http.route(['/get_period'], type='json', website=True, csrf=False)
    def get_periods(self, period, vehicles):

        invoice = request.env['vehicle.rental'].sudo().browse(int(vehicles))
        print(invoice)
        print(vehicles)
        for rec in invoice.rental_charges_ids:
            if rec.time in period:
                amt = rec.amount
                print(amt)
                vals = {
                    'rent_amount': amt
                }
                print(vals)
        return vals
