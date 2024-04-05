# -*- coding: utf-8 -*-
"""
Inherited stock.move.line model for modifying the functionality like adding field and modifying
some existing methods.
@author : Haresh Mori on dated 10-Now-2021
"""
import logging
from odoo import fields, models, api

_logger = logging.getLogger(__name__)


class StockMoveLineEpt(models.Model):
    """
    This class will inherit stock.move.line
    - Functionality:
        - Field: expected_qty, picking_type_code
    @author : Haresh Mori on dated 10-Now-2021
    """
    _inherit = "stock.move.line"

    # Added Field for adding ASN with expected quantity.
    expected_qty = fields.Float(default=0.0, string='Expected Quantity',
                                help='Expected quantity based on tolerance')
