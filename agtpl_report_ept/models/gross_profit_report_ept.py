# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, fields, tools


class GrossProfitReportEpt(models.Model):
    """
    Product Variant
    """
    _name = 'gross.profit.report.ept'
    _description = "Gross Profit Analysis Report"

    product_id = fields.Many2one('product.product')
    actual_revenue = fields.Float()
    total_revenue = fields.Float(string="Total Revenue (%)",digits=(12, 6))
    actual_variable_cost = fields.Float(string="Actual Vaiable Cost")
    total_variable_cost = fields.Float(string="Total variable cost(%)",digits=(12, 6))
    gross_profit = fields.Float(string="Gross profit(%)")
    total_gross_profit = fields.Float()
    total_per_of_gross_profit = fields.Float(string="% of Total GP ", digits=(12, 6)) 
