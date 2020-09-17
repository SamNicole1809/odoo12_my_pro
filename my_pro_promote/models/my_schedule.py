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
