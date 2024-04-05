# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
"""
Created one model product.process.domination.ept to modify some functionality like adding necessary fields.
@author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
"""
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ProductProcessDominationEpt(models.Model):
    """
    Created one model product.process.domination.ept to modify some functionality like adding necessary
    fields.
    - Functionality
        - Field: name, short_code this field defines product structure.
        - Method: default_get() [Inherit]
            To append short_code to name.
        - Method: _check_default_code() [New]
            Constraint for short code.

    @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
    """
    _name = 'product.process.domination.ept'
    _description = 'Process Domination for product.'

    name = fields.Char('Process Domination Name', required=True)
    short_code = fields.Char(required=True, help='Short code for name', size=1)

    def name_get(self):
        """
        To append short_code to name.
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
        """
        return [(i.id, i.name + " - " + i.short_code) for i in self]

    @api.constrains('short_code')
    def _check_default_code(self):
        """
        Created for set unique constraint for the short_code field
            @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 12 November 2021.
        """
        for record in self:
            if self.search([('id', '!=', record.id), ('short_code', '=', record.short_code)]):
                raise ValidationError(_("Short code: {}  is already exist!\n You can't create duplicate short "
                                      "code".format(record.short_code)))
