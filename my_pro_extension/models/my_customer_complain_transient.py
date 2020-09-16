# -*- coding:utf-8 -*-

from odoo import models, api
from odoo.exceptions import UserError


class MyCustomerComplainTransient(models.TransientModel):
    _name = 'my.customer.complain.transient'
    _description = '批量确认'

    # 预处理方法
    @api.model
    def default_get(self, fields_list):
        records = self._get_all_complains(self._context['active_ids'])
        records_undraft_names = records.filtered(lambda r: r.state != 'draft').mapped('name')
        if records_undraft_names:
            raise UserError('下列订单状态不符: \n%s\n请选择未处理的清单' % ','.join(records_undraft_names))
        return super().default_get(fields_list)

    def action_confirm(self):
        records = self._get_all_complains(self._context['active_ids'])
        records.write({'state': 'done'})

    def _get_all_complains(self, record_ids):
        return self.env['my.customer.complain'].search([('id', 'in', record_ids)])