# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _get_partner_search_domain(self):
        """
        Prepare a domain according to customer and vendor search.
        """
        ctx = self._context.copy()
        domain = []
        if ctx.get('res_partner_search_mode') == 'customer' and ctx.get('search_default_customer') != 1:
            ctx.update({'search_default_customer': 1})
            domain = domain + [('customer_rank', '>', 0)]
        elif ctx.get('res_partner_search_mode') == 'supplier' and ctx.get('search_default_supplier') != 1:
            ctx.update({'search_default_supplier': 1})
            domain = domain + [('supplier_rank', '>', 0)]
        self = self.with_context(ctx)
        return domain

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args + self._get_partner_search_domain()
        res = super(ResPartner, self).name_search(
            name, args, operator, limit=limit)
        if not name:
            return res
        return res

    @api.model
    def search_read(self, domain=[], fields=None, offset=0, limit=None, order=None):
        """
        - Updated the Search read method for res.partner model.
        - In general, We will add context filter for the Suppliers and Customers.
        - In customers screen no one can see the suppliers, vice-versa for suppliers no one
        can see the customers in supplier screen.
        @author: Haresh Mori @Emipro Technologies Pvt. Ltd on date 16 December 2021 .
        Task_id: 180987 - Customer & Vendor filter
        """

        domain = domain + self._get_partner_search_domain()
        res = super(ResPartner, self).search_read(domain=domain,
                                                  fields=fields,
                                                  offset=offset, limit=limit,
                                                  order=order)
        return res

class ResUsers(models.Model):
    _inherit = 'res.users'

    def _can_import_remote_urls(self):
        """ Hook to decide whether the current user is allowed to import
        images via URL (as such an import can DOS a worker). By default,
        allows the administrator group.

        :rtype: bool
        """
        self.ensure_one()
        user = self._is_superuser() or self.has_group('base.group_erp_manager') or self.has_group(
                'sales_team.group_sale_manager') or self.has_group('purchase.group_purchase_manager') or self.has_group('stock.group_stock_manager')
        return user