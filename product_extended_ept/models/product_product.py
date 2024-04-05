# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
"""
Inherited one model product.product to modify some functionality like modifying necessary fields
like barcode or some existing methods.

@author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
"""

from odoo import api, fields, models
from odoo.exceptions import ValidationError
import string
import random


class ProductProductEpt(models.Model):
    """
    Inherited one model product.product to modify some functionality like modifying necessary fields
    like barcode or some existing methods.

    - Functionality
        - Field: barcode [Inherit]
            Field Inherited and added one parameter `track_visibility` for that,
            When any user changing barcode then it will post a message in chatter_box.

        - Method: generate_internal_reference() [New]
            This method will create sequence for the product's internal reference
        - Method: _check_default_code() [New]
            Added constraint for default_code

    @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
    """
    _inherit = 'product.product'

    # Field Inherited and added one parameter `track_visibility` for that,
    # When any user changing barcode then it will post a message in chatter_box.
    barcode = fields.Char(tracking=True)

    @api.model
    def create(self, values):
        """
        Inherited for generating sequence id incremental order.
        :return:res (Super Call for create() in-built method.)
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
        """
        res = super(ProductProductEpt, self).create(values)
        # res.generate_barcode()
        res.generate_internal_reference()
        return res

    def generate_internal_reference(self):
        """
        This method will create sequence for the product's internal reference and barcode also.
        **Barcode: Barcode will be generated only when the Fabric features are set.
        - Generate barcode and sku based on the fabric feature.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
        """
        for record in self:
            short_code = ''.join([record.product_structure_id.short_code or '',
                                  record.product_fiber_domination_id.short_code or '',
                                  record.product_process_domination_id.short_code or '', ])
            internal_code_sequence = self.env.ref(
                'product_extended_ept.seq_internal_reference_name').next_by_id()
            prefix = random.choice(string.ascii_uppercase)
            padding_no = internal_code_sequence
            default_code = prefix + short_code
            # Generate the default code with fabric feature with fabric feature count and add 0
            # accordingly.
            if short_code:
                default_code = default_code if len(short_code) == 3 else default_code + '0' if len(
                    short_code) == 2 else default_code + '00' if len(short_code) == 1 else ''

            record.default_code = default_code + padding_no
            # Barcode Format: 21-SKU-00000
            if short_code and default_code:
                record.barcode = "21" + record.default_code + "00000"

    @api.constrains('default_code')
    def _check_default_code(self):
        """
        Created for set constraint for the default code field
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
        """
        for record in self:
            if record.default_code and self.search(
                [('id', '!=', record.id), ('default_code', '=', record.default_code)]):
                raise ValidationError('Duplicate record creation is not allowed !!!\n '
                                      'Internal Reference : {}'.format(record.default_code))
