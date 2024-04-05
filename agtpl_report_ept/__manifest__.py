# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    # App information

    'name': "AGTPL Report Ept",
    'version': '15.0',
    'summary': 'AGTPL Report Ept',
    'category': 'Other',
    'sequence': 0,
    'license': 'OPL-1',

    # Dependencies for any module necessary for this one to work correctly
    'depends': ['point_of_sale', 'sale', 'purchase'],

    # Views
    'data': [
        'security/ir.model.access.csv',
        'report/pos_session_payment.xml',
        'report/pos_session_sale_report.xml',
        'report/invoice_report.xml',
        'report/sale_report_templates.xml',
        'report/delivery_package_report.xml',
        'wizard/gross_profit_report_ept_wiz_view.xml'
    ],

    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical

    'installable': True,
    'auto_install': False,
}
