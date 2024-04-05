# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
"""
Inherited stock.picking model for modifying the functionality like Reset Imported pickings,
Picking validation customization, etc.
@author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021.
"""
from odoo import fields, models
from odoo.tools import logging

_logger = logging.getLogger(__name__)


class PickingEpt(models.Model):
    """
    This class will inherit stock.picking model for modifying the functionality.
    - Functionality
        - Field: import_asn_flag [New]
            Used to set-reset when Picking is imported, reset, etc operations.

        - Method: button_reset_asn() [New]
            Used to reset moves of the pickings if the `import_asn_flag` is true.
        - Method: button_validate() [Inherit]
            Method inherited from ``stock.picking`` for extend some extra feature,
            It will raise error when tolerance level is not equal.

        - Method: action_generate_backorder_wizard() [Inherit]
            Create backorder if the custom flag `imported_picking` is True.

        - Method: _get_overprocessed_stock_moves() [Inherit]
            It will not process the over-processed qty if the custom flag `imported_picking` is
            true.

    @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 9 November 2021 .
    """
    _inherit = 'stock.picking'

    import_asn_flag = fields.Boolean('ASN Imported?', copy=False)

    def button_reset_asn(self):
        """
        This method is used to reset move line if any of the ASN imported by mistake.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 10 November 2021 .
        Task_id: 179613 - ASN functionality development
        """
        if self.import_asn_flag:
            for move_id in self.move_ids_without_package:
                move_line_ids = move_id.move_line_ids.filtered(lambda ml: ml.expected_qty)
                if move_line_ids:
                    move_line_ids.mapped('result_package_id').write({'is_assigned': False})
                    move_line_ids.unlink()
                    self.import_asn_flag = False
            self.action_assign()
