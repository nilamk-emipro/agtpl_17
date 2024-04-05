# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Purchase(models.Model):
    """
    Sale Order
    """
    _inherit = 'purchase.order'
    report_grids = fields.Boolean(
        string="Report Print Variant Grids", default=False,
        help="If set, the matrix of the products configurable by matrix will be shown on the "
             "report of the order.")
