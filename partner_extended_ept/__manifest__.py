# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    # App information

    'name': "Partner Extended Ept",
    'version': '15.0',
    'summary': 'Partner Extended Ept',
    'license': 'OPL-1',
    'category': 'Other',
    'sequence': 0,

    # Dependencies for any module necessary for this one to work correctly
    'depends': ['contacts', 'sale_management', 'purchase', 'account'],

    # Views that will always loaded
    'data': [
        'views/purchase_view.xml',
        'views/res_partner_actions.xml',
        'views/contact_view_ept.xml',
        'views/sale_view.xml',
        'security/bank_detail_security.xml',
    ],
    # Author

    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'http://www.emiprotechnologies.com',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',

    # Technical

    'installable': True,
    'auto_install': False,
}
