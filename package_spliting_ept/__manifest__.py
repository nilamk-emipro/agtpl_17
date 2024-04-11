# -*- coding: utf-8 -*-
{
    'name': "Package Spliting Extended",

    'summary': """Package Spliting Extended""",

    'description': """
        Barcode Extended to add the functionality of generating the package spliting barcode.
    """,
    'license': 'OPL-1',

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Mobile',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock_barcode', 'point_of_sale','stock_delivery'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/res_groups.xml',
        # 'views/stock_quant_views.xml',
        'views/views.xml',
        # 'views/view_stock_location.xml',
        # 'views/templates.xml',
        # 'reports/package_spliting_barcode_report.xml',
        # 'views/weighted_barcode_view.xml',
    ],
    # 'qweb': [
    #     "static/src/xml/barcode_scan_templates.xml",
    # ],
    'assets': {
        'web.assets_backend': [
            'package_spliting_ept/static/src/**/*.js',
            # 'package_spliting_ept/static/src/**/*.scss',
            'package_spliting_ept/static/src/**/*.xml',
        ],
    },
}
