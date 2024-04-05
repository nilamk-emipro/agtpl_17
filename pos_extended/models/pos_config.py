# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    store_short_code = fields.Char('Short Code', help='Store Short code.')
    pos_sequence_id = fields.Many2one('ir.sequence')
    auth_salesman_selection = fields.Boolean("Authorized Salesman")
    authorized_salesman_ids = fields.Many2many('hr.employee', 'pos_salesman', string='Salesman Selection',
                                           help='This is salesman selection for efforts.')
