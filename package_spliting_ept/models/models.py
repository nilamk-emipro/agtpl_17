# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_round
import urllib


class PackageSplitingEpt(models.Model):
    _name = 'package.spliting.barcode'

    @api.model
    def read_barcode(self, barcode):
        """
        Func:
            - Read Barcode from JS.
            - Pass the dictionary to JS of Barcode related details.

        """
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
        return {
            'name': [package.id, package.name],
            'product': product,
            'lot': lot,
            'quantity': quantity,
            'uom': uom,
            'database': self._cr.dbname
        }

    @api.model
    def create_picking(self, package_details):
        if package_details.get('package', '') and package_details.get('package', '').isdigit():
            package = int(package_details.get('package', ''))
        else:
            package = package_details.get('package', '')
        package = self.env['stock.quant.package'].browse(package)
        product = package_details.get('product', '').split(',')
        product_id = self.env['product.product'].browse(int(product[0]))
        product_uom = product_id.uom_id
        lot = package_details.get('lot', '')

        quantity_to_cut = package_details.get('quantity_to_cut', '')
        # vals = {
        #     'name': _('Auto processed move : %s') % product_id.display_name,
        #     'company_id': package.location_id.company_id.id,
        #     'product_id': product_id.id if product else False,
        #     'product_uom_qty': int(quantity_to_cut),
        #     'product_uom': product_uom.id if product_uom else False,
        #     'location_id': int(package_details.get('location_id')),
        #     'location_dest_id': package.location_id.id,
        #     'state': 'confirmed',
        # }
        # stock_move = self.env['stock.move'].create(vals)
        # stock_move._action_assign()
        # stock_move._set_quantity_done(int(quantity_to_cut))
        # stock_move.move_line_ids.write({'result_package_id': package.id})
        # stock_move._action_done()

        picking = self.env['stock.picking'].create({
            'picking_type_id': package.location_id.warehouse_id.int_type_id.id,
            'location_id': package.location_id.id,
            'location_dest_id': package.location_id.id,
            'move_lines': [(0, 0, {
                'name': _('Auto processed move : %s') % product_id.display_name,
                'product_id': product_id.id if product else False,
                'product_uom': product_uom.id if product_uom else False,
                'product_uom_qty': quantity_to_cut,
                'location_id': package.location_id.id,
                'location_dest_id': package.location_id.id,
                'state': 'confirmed',
            })],
        })
        stock_move = picking.move_lines
        # stock_move._action_assign()
        stock_move._set_quantity_done(float(quantity_to_cut))
        stock_move.move_line_ids.write({'package_id': package.id})
        # stock_move._action_done()

        # picking.action_confirm()
        picking.with_context(barcode_view=True).action_put_in_pack()
        picking.button_validate()

        return {'barcode_id': picking.package_ids[0].id,
                'barcode': picking.package_ids.name,
                'remaining_qty': package.quant_ids[0].quantity}
