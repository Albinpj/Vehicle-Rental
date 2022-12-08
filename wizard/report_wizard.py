import json
import io
import xlsxwriter
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import date_utils


class CreateReportWizard(models.TransientModel):
    _name = 'create.report.wizard'
    _description = 'CreateReportWizard '

    date_from = fields.Date(string="From Date")
    date_to = fields.Date(strreporting="To Date")
    vehicle_id = fields.Many2one('vehicle.rental')

    def action_print_report(self):
        var = ("""SELECT res_partner.name as pname,fleet_vehicle_model.name as vname,period,vehicle_rental.state 
        from vehicle_request
        inner join vehicle_rental on vehicle_rental.id=vehicle_request.vehicle_id
        inner join fleet_vehicle on fleet_vehicle.id=vehicle_rental.vehicle_id
        inner join fleet_vehicle_model on fleet_vehicle_model.id=fleet_vehicle.model_id
        inner join res_partner  on vehicle_request.customer_id=res_partner.id""")
        if self.date_from:
            new_var = """ and request_date >= '%s' """ % self.date_from
            var += new_var

        if self.date_to:
            new_var = """ and request_date <= '%s' """ % self.date_to
            var += new_var

        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValidationError('From Date And To Date Is Reversible')

        if self.vehicle_id:
            new_var = """ and vehicle_request.vehicle_id = '%s' """ % self.vehicle_id.id
            var += new_var
        print(var)
        self.env.cr.execute(var)
        record = self.env.cr.dictfetchall()
        print(record)
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'vehicle_id': self.vehicle_id.name,
            'query': record
        }
        return self.env.ref('vechile_rental.action_vehicle_report').report_action(None, data=data)

    def action_print_xls_report(self):
        var = ("""SELECT res_partner.name as pname,fleet_vehicle_model.name as vname,period,vehicle_rental.state 
        from vehicle_request
        inner join vehicle_rental on vehicle_rental.id=vehicle_request.vehicle_id
        inner join fleet_vehicle on fleet_vehicle.id=vehicle_rental.vehicle_id
        inner join fleet_vehicle_model on fleet_vehicle_model.id=fleet_vehicle.model_id
        inner join res_partner  on vehicle_request.customer_id=res_partner.id""")
        if self.date_from:
            new_var = """ and request_date >= '%s' """ % self.date_from
            var += new_var

        if self.date_to:
            new_var = """ and request_date <= '%s' """ % self.date_to
            var += new_var

        if self.date_from and self.date_to:
            if self.date_from > self.date_to:
                raise ValidationError('From Date And To Date Is Reversible')

        if self.vehicle_id:
            new_var = """ and vehicle_request.vehicle_id = '%s' """ % self.vehicle_id.id
            var += new_var
        self.env.cr.execute(var)
        record = self.env.cr.dictfetchall()
        print(record)
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'vehicle_id': self.vehicle_id.name,
            'query': record
        }
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'create.report.wizard',
                     'options': json.dumps(data, default=date_utils.json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format({'font_size': '12px', 'bold': True})
        head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px'})
        sheet.merge_range('D2:J3', 'VEHICLE RENTAL REPORT', head)
        sheet.write('B6', 'From:', cell_format)
        sheet.merge_range('C6:D6', data['date_from'], txt)
        sheet.write('F6', 'To:', cell_format)
        sheet.merge_range('G6:H6', data['date_to'], txt)
        sheet.write('B7', 'Vehicle:', cell_format)
        sheet.merge_range('C7:E7', data['vehicle_id'], txt)

        sheet.write('A11:B11', 'Sl no', cell_format)
        sheet.write('B11:D11', 'Customer Name', cell_format)
        sheet.write('E11:F11', 'Model', cell_format)
        sheet.write('G11:H11', 'No Of Days', cell_format)
        sheet.write('I11:J11', 'State', cell_format)

        row = 11
        column = 0
        a = 1
        for i in data['query']:
            sheet.write(row, column, a)
            a = a + 1
            sheet.write(row, column + 1, i['pname'])
            sheet.write(row, column + 4, i['vname'])
            sheet.write(row, column + 6, i['period'])
            sheet.write(row, column + 8, i['state'])
            row += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
