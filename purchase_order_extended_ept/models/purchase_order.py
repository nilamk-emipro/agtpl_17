from odoo import models, fields, _, api
import json

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    vendor_packing_instruction = fields.Char()
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    has_pre_export_vendor = fields.Boolean(string="Has Pre Export Vendor",
                                           help="Has Pre Export Vendor")
    pre_export_vendor = fields.Many2one(string="Pre Export Vendor", comodel_name='res.partner')
    total_pre_export_vendor_amount = fields.Float(string="Total PEV (CNY)",
                                                 compute='_compute_total_pre_export_vendor_amount',
                                                 help="Total Pre Export Vendor Amount")

    @api.depends('order_line.pre_export_vendor_amount')
    def _compute_total_pre_export_vendor_amount(self):
        total = 0.0
        for order in self.order_line:
            total += order.pre_export_vendor_amount
        self.total_pre_export_vendor_amount = total


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    pre_export_vendor_unit_price = fields.Float(string="Pre Export Vendor Unit Price",
                                                help="Pre Export Vendor Unit Price")
    pre_export_vendor_amount = fields.Float(string="Pre Export Vendor Amount",
                                            help="Pre Export Vendor Amount",
                                            compute='_compute_pre_export_vendor_amount')
    vendor_packing_instruction = fields.Char()

    @api.depends('pre_export_vendor_unit_price', 'price_unit')
    def _compute_pre_export_vendor_amount(self):
        for order_line in self:
            order_line.pre_export_vendor_amount = order_line.product_qty * order_line.pre_export_vendor_unit_price

    def _product_id_change(self):
        res = super(PurchaseOrderLine,self)._product_id_change()
        self.vendor_packing_instruction = self.product_id.vendor_packing_instruction