# -*- coding:utf-8 -*-

from odoo import fields, models


# 销售模块扩展
class SaleOrderExtension(models.Model):
    """销售模块扩展"""
    _inherit = 'sale.order'

    # 销售员
    x_salesman = fields.Many2one(
        'res.users',
        string='销售员',
        related='partner_id.user_id'
    )
