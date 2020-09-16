# -*- coding:utf-8 -*-

from odoo import fields, models


class MyCustomerComplainType(models.Model):
    _name = 'my.customer.complain.type'
    _description = '客户投诉类型'

    name = fields.Char('投诉类型')

    number = fields.Integer('数量', default=0, compute='_get_type_complain_number')

    def _get_type_complain_number(self):
        for record in self:
            record.number = record.env['my.customer.complain'].search_count(
                [('type_id', '=', record.id), ('state', '=', 'done')])

    def _get_action(self, action_xmlid):
        action = self.env.ref(action_xmlid).read()[0]
        if self:
            action['display_name'] = self.display_name
        return action

    def go_complains(self):
        return self._get_action('my_pro_extension.action_go_my_customer_complains')
