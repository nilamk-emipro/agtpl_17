# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class StockPackageType(models.Model):
    _inherit = "stock.package.type"

    package_weight = fields.Float()
