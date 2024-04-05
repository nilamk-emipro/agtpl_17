{
    'name': 'POS Extended',
    'version': '15.0.1.1',
    'license': 'OPL-1',
    'category': 'Sales/Point of Sale',
    'summary': '',
    'depends': ['point_of_sale'],
    'data': [],
    'demo': [],
    'installable': True,
    'application': True,
    'author': 'Emipro Technologies Pvt. Ltd.',
    'website': 'https://www.emiprotechnologies.com/',
    'maintainer': 'Emipro Technologies Pvt. Ltd.',
    'data': [
            'views/res_config.xml',
            'views/pos_order.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'web/static/lib/zxing-library/zxing-library.js',
            'pos_extended/static/src/js/Screens/PaymentScreen/PaymentScreen.js',
            'pos_extended/static/src/js/Screens/ClientListScreen/ClientListScreen.js',
            'pos_extended/static/src/js/Screens/ReceiptScreen/ReceiptScreen.js',
            'pos_extended/static/src/js/Screens/ProductScreen/ProductScreen.js',
            'pos_extended/static/src/js/models.js',
            'pos_extended/static/src/js/Screens/ProductScreen/ControlButtons/SetSalesmanButton.js',
            'pos_extended/static/src/js/Screens/ProductScreen/ControlButtons/SetEffortButton.js',

        ],
        'web.assets_backend': [
            ('replace', 'web/static/src/webclient/actions/action_service.js',
             'pos_extended/static/src/js/action_manager_extend.js'),
        ],
        'web.assets_qweb': [
            'pos_extended/static/src/xml/OrderReceipt.xml',
            'pos_extended/static/src/xml/ClientDetailsEdit.xml',
            'pos_extended/static/src/xml/Screens/ProductScreen/ControlButtons/SetSalesmanButton.xml',
            'pos_extended/static/src/xml/Screens/ProductScreen/ControlButtons/SetEffortButton.xml',
        ],
    }
}
