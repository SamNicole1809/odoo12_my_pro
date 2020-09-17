# -*- coding:utf-8 -*-

from odoo import models, fields

import asyncio


class MySchedule(models.AbstractModel):
    _name = 'my.schedule'
    _description = '定时任务'

    def schedule(self):
        start_time = fields.datetime.now()
        asyncio.run(self.do_schedule_list())
        end_time = fields.datetime.now()
        print('cost time =>', end_time - start_time)
        # self.test_high_order_func()

    # odoo高阶函数测试
    def test_high_order_func(self):
        records = self.env['my.customer.complain'].search([])

        # 记录对象.mapped()的用法
        # 获取所有记录的state字段
        print(records.mapped('state'))
        # ['done', 'done', 'cancel', 'done', 'done', 'done', 'draft', 'draft']
        print(records.mapped(lambda record: (record.name, record.state)))
        # [('MCC001', 'done'), ('MCC002', 'done'), ('MCC003', 'cancel'), ('MCC004', 'done')...]

        # 记录对象.filtered()的用法
        print(records.filtered(lambda record: record.state == 'draft'))
        # my.customer.complain(9, 10) -> 返回的是多个可迭代的记录对象,不是列表

        # 记录对象.sorted()的用法
        print(records.sorted(key=lambda record: record.name, reverse=True))
        # my.customer.complain(10, 9, 8, 7, 6, 5, 4, 3)

        # 可以多个方法连用
        print(records.filtered(lambda x: x.state == 'done').mapped('name'))
        # ['MCC001', 'MCC002', 'MCC004', 'MCC005', 'MCC006']
        print(records.filtered(lambda x: x.state == 'done').sorted(key=lambda x: x.name, reverse=True).mapped('name'))
        # ['MCC006', 'MCC005', 'MCC004', 'MCC002', 'MCC001']

        # 有的时候还想和Python的高阶函数连用
        print(sorted(records.mapped('name'), key=lambda x: x, reverse=True))
        # ['MCC008', 'MCC007', 'MCC006', 'MCC005', 'MCC004', 'MCC003', 'MCC002', 'MCC001']

        record_list = [record for record in records]
        # odoo自带的高阶函数,只能使用odoo本身的可迭代对象
        # 对于我们自己构建的列表,应使用Python原有的高阶函数
        # 以下情况均报错
        # print(record_list.mapped('id'))
        # print(record_list.filtered(lambda record: record.state == 'draft'))
        # print(record_list.sorted(key=lambda record: record.name, reverse=True))
        # -------- 错误分割线 --------
        print(map(lambda x: x.name, record_list))
        # <map object at 0x000001DFCF42E048>
        print(filter(lambda x: x.state == 'draft', record_list))
        # <filter object at 0x000001DFCF42E048>
        print(sorted(record_list, key=lambda x: x.name, reverse=True))
        # [my.customer.complain(10,), my.customer.complain(9,), my.customer.complain(8,)...]
        print([x for x in
               map(lambda x: x.name, sorted(filter(lambda x: x.state == 'draft', record_list), key=lambda x: x.name))])
        # ['MCC007', 'MCC008']

        # python原有的高阶函数可以处理odoo的记录集(不推荐)
        print(sorted(records, key=lambda x: x.name, reverse=True))
        # [my.customer.complain(10,), my.customer.complain(9,), my.customer.complain(8,)...]
        print(map(lambda x: x.name, records))
        # <map object at 0x00000295F9C5BF60>
        print(filter(lambda x: x.state == 'draft', records))
        # <filter object at 0x00000295F9C5BF60>

    # 任务列表,可能有多个定时任务需要执行,每个任务前加await
    async def do_schedule_list(self):
        await self.statistics_compute_sum_nums()

    # 具体的定时任务,这里是求和任务,1-100的和
    async def statistics_compute_sum_nums(self):
        # 定义异步方法列表,有三个异步任务
        tasks = [
            asyncio.create_task(self._compute_sum_nums(1, 30)),
            asyncio.create_task(self._compute_sum_nums(30, 60)),
            asyncio.create_task(self._compute_sum_nums(60, 101))
        ]
        # gather会异步执行任务,并返回所有任务完成后的结果
        result = await asyncio.gather(*tasks)
        print('result=>', result, 'sum=>', sum(result), 'time=>', fields.datetime.now())

    # 耗时方法
    async def _compute_sum_nums(self, start, end):
        await asyncio.sleep(2)
        return sum(range(start, end))
