{
    'name': 'Rental',
    'version': '15.0.5.0',
    'category': 'Rental',
    'sequence': -500,
    'summary': 'Vehicle Rental',
    'application': True,
    'depends': [
        'base',
        'fleet',
        'account',
        'mail',
        'website',

    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/report_wizard.xml',
        'view/menu.xml',
        'view/submenu.xml',
        'view/rental_views.xml',
        'view/fleet.xml',
        'view/request_views.xml',
        'data/sequence.xml',
        'data/warning_late.xml',
        'report/vehicle_report.xml',
        'report/vehicle_template.xml',
        'view/rent_request_website.xml',
        'view/rent_request_website_template.xml',
        'view/rental_request_customer.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'vechile_rental/static/src/js/action_manager.js'],
        'web.assets_frontend': [
            'vechile_rental/static/src/js/rent_request_website.js'],
    }

}
