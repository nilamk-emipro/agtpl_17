# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero


class GrossProfitReportEpt(models.TransientModel):
    _name = "gross.profit.report.ept.wiz"
    _description = "Gross Profit Report Wizard"

    from_date = fields.Date('Date From', required=True)
    to_date = fields.Date('Date To', required=True, default=fields.Date.context_today)

    def generate_gross_profit_report(self):
        if self.from_date > self.to_date:
            raise UserError(_("Please select From date less then the To date"))
        result = self._get_gross_profit_data(self.from_date, self.to_date)
        if result:
            self._set_data_of_gross_profit_report(result)
        return {
            'name': 'Gross Profit Report',
            'view_type': 'form',
            'view_mode': 'pivot',
            'view_id': self.env.ref('agtpl_report_ept.gross_profit_pivot_report').id,
            'res_model': 'gross.profit.report.ept',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
        }

    def _get_gross_profit_data(self, from_date, to_date):
        qry = f"""select product_id, sum(product_uom_qty) as product_uom_qty, sum(price_total) as price_total from
                        (Select sol.product_id,sum(sol.product_uom_qty) as product_uom_qty,sum(sol.price_total) as price_total from sale_order_line sol 
                        Left JOIN sale_order so on so.id = sol.order_id
                        where date(so.date_order) >= '{from_date}' AND date(so.date_order) <= '{to_date}' AND so.state in ('sale', 'done', 'paid') group by sol.product_id
                        UNION ALL
                        Select pol.product_id,sum(pol.qty) as product_uom_qty,sum(pol.price_subtotal) as price_total from pos_order_line pol 
                        Left JOIN pos_order po on po.id = pol.order_id
                        where date(po.date_order) >= '{from_date}' AND date(po.date_order) <= '{to_date}' AND po.state in ('paid','invoiced','done') group by pol.product_id
                        )T group by product_id;"""
        self._cr.execute(qry)
        result = self._cr.dictfetchall()
        return result

    def _set_data_of_gross_profit_report(self, result):
        """
        This Method is used to set gross profit report data as per query.
        @author: Meera Sidapara on date 27 Oct 2023.
        @Task: GROSS profit report
        """
        gross_profit_report_obj = self.env['gross.profit.report.ept']
        gross_profit_records = gross_profit_report_obj.search([])
        if gross_profit_records:
            gross_profit_records.unlink()
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        all_product_total_gross_profit = sum(
            [abs(rec.get('price_total') - self.env['product.product'].browse(rec.get('product_id')).standard_price)
             for rec in result])
        total_variable_cost = sum(
            [abs(rec.get('product_uom_qty') * self.env['product.product'].browse(rec.get('product_id')).standard_price)
             for rec in result])
        all_product_total_revenue = sum([rec.get('price_total') for rec in result])
        for record in result:
            product_id = self.env['product.product'].browse(record.get('product_id'))
            if record.get('product_id'):
                product_actual_revenue = record.get('price_total')
                product_total_revenue = 0.0
                total_product_cost = 0.0
                gross_profit = 0.0
                total_per_of_gross_profit = 0.0
                actual_variable_cost = record.get('product_uom_qty') * product_id.standard_price
                total_gross_profit = abs(product_actual_revenue - actual_variable_cost)

                if not float_is_zero(product_actual_revenue, precision_digits=precision) and not float_is_zero(
                        all_product_total_revenue, precision_digits=precision):
                    product_total_revenue = (product_actual_revenue / all_product_total_revenue) * 100

                if not float_is_zero(actual_variable_cost, precision_digits=precision) and not float_is_zero(
                        product_actual_revenue, precision_digits=precision):
                    total_product_cost = (actual_variable_cost / total_variable_cost) * 100

                if not float_is_zero(total_gross_profit, precision_digits=precision) and not float_is_zero(
                        product_actual_revenue, precision_digits=precision):
                    gross_profit = (total_gross_profit / product_actual_revenue) * 100

                if not float_is_zero(total_gross_profit, precision_digits=precision) and not float_is_zero(
                        all_product_total_gross_profit, precision_digits=precision):
                    total_per_of_gross_profit = (total_gross_profit / all_product_total_gross_profit) * 100

                gross_profit_report_obj.create({'product_id': product_id.id, 'actual_revenue': product_actual_revenue,
                                                'total_revenue': product_total_revenue,
                                                'actual_variable_cost': actual_variable_cost,
                                                'total_variable_cost': total_product_cost,
                                                'gross_profit': gross_profit, 'total_gross_profit': total_gross_profit,
                                                'total_per_of_gross_profit': total_per_of_gross_profit})
        return True
