# -*- coding:utf-8 -*-

from odoo import fields, models, api, _


class MyCustomerComplain(models.Model):
    _name = "my.customer.complain"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = '客户投诉'

    name = fields.Char(
        string='编号', default=lambda self: _('New'),
        copy=False, readonly=True, track_visibility='always'
    )

    # 客户
    customer_id = fields.Many2one(
        'res.partner', string='客户',
        domain=[('customer', '=', True), ('parent_id', '=', False)]
    )

    # 供应商
    supplier_id = fields.Many2one(
        'res.partner', string='供应商',
        domain=[('supplier', '=', True), ('parent_id', '=', False)]
    )

    # 销售订单
    order_id = fields.Many2one(
        'sale.order', string='销售订单',
        domain=[('state', '=', 'sale')]
    )

    # 投诉内容
    complains = fields.Text(string='投诉内容')

    type_id = fields.Many2one('my.customer.complain.type', '投诉类型')

    # 状态
    state = fields.Selection(
        [('draft', '未处理'), ('done', '完成'), ('cancel', '取消')],
        string='状态', readonly=True, default='draft', track_visibility='onchange'
    )

    # 颜色--看板用
    color = fields.Integer('颜色')

    @api.model
    def create(self, vals):
        if not vals.get('name') or vals['name'] == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('my.customer.complain') or _('New')
        return super().create(vals)

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        self.state = 'cancel'

    @api.multi
    def action_comfirm(self):
        self.ensure_one()
        self.state = 'done'
