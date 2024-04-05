# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ProductCareLabel(models.Model):
    """
        ProductCareLabel
    """
    _name = 'product.care.label'
    _description = 'Product Care Label'

    name = fields.Char('Name', help='Name of Product Care Label')
    description = fields.Char('Description', help='Description of the Product Care Label')
    label_image = fields.Image(help='Image of the Product Care label.',
                               max_width=50, max_height=50)
