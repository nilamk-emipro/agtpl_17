# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
"""
Inherited one model stock.quant.package to adding some functionality.
@author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 10 November 2021.
"""

from odoo import models, fields, api
from collections import defaultdict


class StockQuantPackageEpt(models.Model):
    """
    Inherited one model stock.quant.package to adding some functionality.
    - Functionality
        - Field: is_assigned: This field will checked if the package was assigned to any pickings.
    @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 10 November 2021.
    """
    _inherit = "stock.quant.package"

    # This field will checked if the package was assigned to any pickings.
    is_assigned = fields.Boolean('Is Assigned?')

    @api.depends('quant_ids')
    def _compute_weight(self):
        if self.env.context.get('picking_id'):
            package_weights = defaultdict(float)
            # Ordering by qty_done prevents the default ordering by groupby fields that can inject multiple Left Joins in the resulting query.
            res_groups = self.env['stock.move.line'].read_group(
                [('result_package_id', 'in', self.ids), ('product_id', '!=', False),
                 ('picking_id', '=', self.env.context['picking_id'])],
                ['id:count'],
                ['result_package_id', 'product_id', 'product_uom_id', 'qty_done'],
                lazy=False, orderby='qty_done asc'
            )
            for res_group in res_groups:
                product_id = self.env['product.product'].browse(res_group['product_id'][0])
                product_uom_id = self.env['uom.uom'].browse(res_group['product_uom_id'][0])
                package_weights[res_group['result_package_id'][0]] += (
                        res_group['__count']
                        * product_uom_id._compute_quantity(res_group['qty_done'], product_id.uom_id)
                        * product_id.weight
                )
        for package in self:
            if self.env.context.get('picking_id'):
                package.weight = package_weights[package.id] + package.package_type_id.package_weight
            else:
                weight = 0.0
                for quant in package.quant_ids:
                    weight += quant.quantity * quant.product_id.weight
                package.weight = weight + package.package_type_id.package_weight
