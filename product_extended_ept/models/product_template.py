# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ProductTemplate(models.Model):
    """
    Inherited one model product.template to modify some functionality like adding extra necessary fields.
    - Functionality
        - Fields: All are the fabric feature.
        - Fields: tracking
            Inherited field to set every new product tracking as `lot`.

    @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
    """
    _inherit = 'product.template'

    # Fields: All are the fabric feature.
    generate_sku = fields.Many2one('product.structure.ept', 'Structure',
                                   help='Process Structure')
    product_fiber_domination_id = fields.Many2one('product.fiber.domination.ept',
                                                  'Fiber Domination', help='Fiber Domination')
    product_process_domination_id = fields.Many2one('product.process.domination.ept',
                                                    'Process Domination',
                                                    help='Process Domination')
    product_structure_id = fields.Many2one('product.structure.ept', 'Product Structure',
                                           help='Product Structure')
    composition = fields.Char('Composition')
    gsm = fields.Float('GSM', help='Grams per square meter')
    warp = fields.Char('Warp')
    weft = fields.Char('Weft')
    epi = fields.Float('EPI')
    ppi = fields.Float('PPI')
    moq = fields.Float('MOQ', help='Minimum Order Quantity for Production')
    product_care_label_m2m_ids = fields.Many2many('product.care.label',
                                                  'product_template_product_care_label_rel',
                                                  string='Product Care Labels')


class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    @api.model
    def create(self, vals):
        if not self._context.get('is_asn_package'):
            if vals.get('name'):
                vals.update({'name': self.env['ir.sequence'].next_by_code('stock.quant.package')})
        return super(StockQuantPackage, self).create(vals)
