# -*- coding: utf-8 -*-
"""
Inherited stock.move for modifying the functionality of that model like adding new necessary
fields with necessary compute method also, and some core functionality of this model.
@author : Haresh Mori on dated 10-Now-2021
"""
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class StockMoveEpt(models.Model):
    """
    This class will inherit stock.move for modifying the functionality of that model like adding
    new necessary fields with necessary compute method also, and some core functionality of this
    model.
    - Functionality
        - Fields: expected_qty, difference, show_expected_qty, etc

        - Compute Method of fields:
            > expected_qty:  _compute_expected_qty()
            > difference: _compute_difference()
            > show_expected_qty: _compute_show_expected_qty()

    @author : Haresh Mori on dated 10-Now-2021
    """
    _inherit = "stock.move"

    # To set expected qty
    expected_qty = fields.Float(compute='_compute_expected_qty', string='Expected Quantity',
                                help='Expected quantity based on tolerance')

    @api.depends('move_line_ids.expected_qty', 'move_line_ids.product_uom_id')
    def _compute_expected_qty(self):
        """
        This field represents the sum of the move lines `expected_qty`. It allows the user to
        know if there is still work to do.
        @author : Haresh Mori on dated 10-Now-2021
        """
        for move in self:
            total_expected_qty = 0
            for move_line in move._get_move_lines():
                total_expected_qty += move_line.product_uom_id._compute_quantity(
                    move_line.expected_qty,
                    move.product_uom,
                    round=False)
            move.expected_qty = total_expected_qty
            _logger.info("Expected_Qty--------------{}".format(move.expected_qty))
            if move.picking_id.picking_type_code == 'internal':
                _logger.info("Picking Type--------------{}, "
                             "Reserved/Expected Quantity--------------"
                             "{}".format(move.picking_id.picking_type_code,
                                         move.reserved_availability))
                move.expected_qty = move.reserved_availability
