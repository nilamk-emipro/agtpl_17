# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models


class POSSession(models.Model):
    """
    POS Session
    """
    _inherit = 'pos.session'

    def _get_report_base_filename(self):
        """
        This method use to get Session Name For Print In POS Session Report
        Task: 187286
        :return: string[Session Name]
        """
        return self.name

    def payment_method_groups(self):
        """
        Searching the data of Total of Amount of Session group by payment methods.
        Task: 187286
        :return: list of dictionary with payment method wise information for session
        """
        return self.env['pos.payment'].read_group(domain=[('session_id', '=', self.id)],
                                                  fields=['payment_method_id', 'amount'],
                                                  groupby=['payment_method_id'])
