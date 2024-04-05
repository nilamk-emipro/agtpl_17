# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields,api


class SaleOrder(models.Model):
    """
    Sale Order
    """
    _inherit = 'sale.order'
    report_grids = fields.Boolean(
        string="Report Print Variant Grids", default=False,
        help="If set, the matrix of the products configurable by matrix will be shown on the "
             "report of the order.")


    @api.model
    def default_get(self,fields):
        res = super(SaleOrder,self).default_get(fields)
        res['report_grids'] = False
        return res