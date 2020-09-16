# -*- coding:utf-8 -*-
"""销售订单行扩展"""

from odoo import models, fields, api


# 销售订单行扩展
class SaleOrderLineExtension(models.Model):
    """销售订单行扩展"""
    _inherit = 'sale.order.line'

    # 税额
    x_price_tax = fields.Monetary(string='税额', compute='_get_line_price_tax')

    # 获取订单行税额
    @api.multi
    def _get_line_price_tax(self):
        """
        获取订单行税额
        :return: None
        """
        if self:
            # self是订单行对象数据集
            # 遍历数据集
            for line in self:
                # 税率
                tax = sum(line.tax_id.mapped('amount')) / 100
                # 单价
                price = line.price_unit
                # 数量
                number = line.product_uom_qty
                # 税额 = 不含税销售额 × 税率
                # 不含税销售额 = 含税价 / （1 + 税率）
                line.x_price_tax = (price / (1 + tax) * tax) * number
