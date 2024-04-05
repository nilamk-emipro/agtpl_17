# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    # App information

    'name': "Stock Extended Ept",
    'version': '15.0.0.0',
    'summary': 'Stock Extended Ept',
    'category': 'Other',
    'sequence': 0,
    'license': 'OPL-1',

    # Dependencies for any module necessary for this one to work correctly
    'depends': ['stock', 'purchase', 'sale', 'delivery'],

    # Views that will always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizards/import_asn_wizard_view_ept.xml',
        'views/res_partner_view_ept.xml',
        'views/stock_move_line_ept_views.xml',
        'views/stock_picking_ept_views.xml',
        'views/stock_package_type_view.xml'
    ],
    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical

    'installable': True,
    'auto_install': False,
}
