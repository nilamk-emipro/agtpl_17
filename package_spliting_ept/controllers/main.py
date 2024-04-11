# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import pdf, split_every
from odoo.tools.misc import file_open


class PackageBarcodeController(http.Controller):

    @http.route('/package_spliting_ept/get_barcode_data', type='json', auth='user')
    def get_barcode_data(self, model, barcode):
        """ Returns a dict with values used by the barcode client:
        {
            "data": <data used by the stock barcode> {'records' : {'model': [{<record>}, ... ]}, 'other_infos':...}, _get_barcode_data_prefetch
            "groups": <security group>, self._get_groups_data
        }
        """
        data = request.env[model].read_barcode(barcode)
        return data

    @http.route('/package_spliting_ept/create_picking', type='json', auth='user')
    def create_picking(self, model, form_data):
        """ Returns a dict with values used by the barcode client:
        {
            "data": <data used by the stock barcode> {'records' : {'model': [{<record>}, ... ]}, 'other_infos':...}, _get_barcode_data_prefetch
            "groups": <security group>, self._get_groups_data
        }
        """
        data = request.env[model].create_picking(form_data)
        return data
