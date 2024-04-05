# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
"""
Inherited one model res.partner for modifying the functionality like adding name_short_code and
modify the write method.
@author : Haresh Mori on dated 10-Now-2021
"""
from odoo import fields, models, api


class ResPartnerEpt(models.Model):
    """
    Inherited one model res.partner for modifying the functionality like adding name_short_code and
    modify the write method.
    - Functionality
        - Field: name_short_code short code of vendor name.
    @author : Haresh Mori on dated 10-Now-2021
    """
    _inherit = 'res.partner'

    name_short_code = fields.Char(string='Short Code',
                                  help='Short code of Vendor name', tracking=True)
    first_order_date = fields.Date(compute='_get_customer_history_data', store=True)
    last_order_date = fields.Date(compute='_get_customer_history_data', store=True)
    total_sales = fields.Float(compute='_get_customer_history_data', default=0.0, store=True)
    average_order_per_month = fields.Float(compute='_get_customer_history_data', default=0.0, store=True)

    @api.model
    def create(self, vals):
        if self._context.get('res_partner_search_mode') == 'supplier':
            vals['name_short_code'] = self.env['ir.sequence'].sudo().next_by_code('vendor.code') or '/'
        return super(ResPartnerEpt, self).create(vals)

    @api.depends('invoice_ids','sale_order_count','pos_order_count','invoice_ids.state')
    def _get_customer_history_data(self):
        for customer in self:
            sale_orders = customer.invoice_ids.filtered(lambda l : l.state not in ['draft','cancel'] and l.move_type == 'out_invoice')
            customer.first_order_date = False
            customer.last_order_date = False
            total_sales = []
            if sale_orders:
                total_sales.extend(sale_orders.mapped('amount_total'))
                customer.first_order_date = sale_orders.mapped('invoice_date')[-1]
                customer.last_order_date = sale_orders.mapped('invoice_date')[0]

            customer.total_sales = sum(total_sales)
            first_order_date = customer.first_order_date
            last_order_date = customer.last_order_date
            customer.average_order_per_month = customer.total_sales
            if first_order_date and last_order_date:
                months = (last_order_date.year - first_order_date.year) * 12 + (
                        last_order_date.month - first_order_date.month)
                if customer.total_sales and months:
                    customer.average_order_per_month = customer.total_sales / months
