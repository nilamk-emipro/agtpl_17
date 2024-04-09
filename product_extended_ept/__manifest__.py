# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    # App information

    'name': "Product Extended Ept",
    'version': '0.1',
    'summary': 'Product Extended Ept',
    'category': 'Other',
    'sequence': 0,
    'license': 'OPL-1',

    # Dependencies for any module necessary for this one to work correctly
    'depends': ['product', 'stock'],

    # Views that will always loaded
    'data': [
        'data/sku_barcode_sequence.xml',
        'security/ir.model.access.csv',
        'views/product_product_view_ept.xml',
        'views/product_template_view.xml',
        'views/product_care_label_view.xml'
    ],
    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical

    'installable': True,
    'auto_install': False,
}
