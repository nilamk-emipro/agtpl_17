# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import pdf, split_every
from odoo.tools.misc import file_open


class StockBarcodeController(http.Controller):

    @http.route('/package_barcode/scan_from_package_splitting', type='json', auth='user')
    def main_menu(self, barcode):
        """ Receive a barcode scanned from the main menu and return the appropriate
            action (open an existing / new picking) or warning.
        """

        # barcode_type = None
        # nomenclature = request.env.company.nomenclature_id
        # if nomenclature.is_gs1_nomenclature:
        #     parsed_results = nomenclature.parse_barcode(barcode)
        #     if parsed_results:
        #         for result in parsed_results[::-1]:
        #             if result['rule'].type in ['product', 'package', 'location', 'dest_location']:
        #                 barcode_type = result['rule'].type
        #                 break
        # if not barcode_type or barcode_type == 'package':
        #     package = request.env['stock.quant.package'].search([('name', '=', barcode), ('quant_ids', '!=', False)],
        #                                                         limit=1)

        if not barcode:
            return {'error': "Please, Scan the barcode !!"}
        package = self.env['stock.quant.package'].search([('name', '=', barcode), ('quant_ids', '!=', False)], limit=1)
        if not package:
            return {'error': "No package found for the scanned barcode. Please try again!"}
        product = [package.quant_ids.product_id.id, package.quant_ids.product_id.display_name.replace(",", "."),
                   package.quant_ids.product_id.barcode]
        lot = [package.quant_ids.lot_id.id, package.quant_ids.lot_id.name]
        quantity = sum(package.quant_ids.mapped('quantity'))
        uom = [package.quant_ids.product_uom_id.id, package.quant_ids.product_uom_id.name]
        if package:
            view_id = request.env.ref('package_spliting_ept.view_package_splitting_form').id
            return {
                'action': {
                    'name': 'Open package',
                    'res_model': 'package.spliting.barcode',
                    'views': [(view_id, 'form')],
                    'type': 'ir.actions.act_window',
                    'res_id': package.id,
                    'context': {'active_id': package.id,
                                'name': [package.id, package.name],
                                'product': product,
                                'lot': lot,
                                'quantity': quantity,
                                'uom': uom,
                                'database': self._cr.dbname}
                }
            }
