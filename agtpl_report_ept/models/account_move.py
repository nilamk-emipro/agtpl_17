# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_net_weight(self):
        self.ensure_one()
        net_weight = 0.0
        for line in self.invoice_line_ids:
            net_weight += line.product_id.weight * line.quantity
        return net_weight
