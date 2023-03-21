"""crawlers"""
import asyncio

from example import settings

from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from tests.example.utils import DemoRequest


class DemoCrawlers:
    """DemoCrawlers"""
    url = 'http://localhost:8000/api/v1/example'

    def __init__(self):
        self.metrics_task = None
        self.sdk = SpiderkeeperSDK(
            task_name=settings.TASK_NAME,
            data_url=settings.DATA_URL,
            log_url=settings.LOG_URL,
            metrics_url=settings.METRICS_URL,
            storage_enable=bool(settings.STORAGE_ENABLE),
            snapshot_enable=bool(settings.SNAPSHOT_ENABLE),
        )
        self.request = DemoRequest()

    async def init_metrics_collector_task(self):
        """
        由爬虫程序初始化监控指标收集任务
        :return:
        """
        loop = asyncio.get_running_loop()
        self.metrics_task = loop.create_task(self.sdk.metrics())
        await asyncio.sleep(3)

    async def crawlers(self):
        """crawlers"""
        # 发送日志
        await self.sdk.logs(f'Crawler {self.url}')
        res = await self.request.req_get(self.url)
        await self.init_metrics_collector_task()
        # 发送数据
        await self.send_data(res.json())
        self.metrics_task.cancel()
        await asyncio.sleep(5)

    async def send_data(self, data):
        """send data"""
        await self.sdk.send_data(data=data)

    def __del__(self):
        if self.metrics_task and self.metrics_task.done():
            self.metrics_task.cancel()
    # def stop(self):
    #     """"""
    #     asyncio.create_task(self.check_task())
    #
    # def check_task(self):
    #     """check task"""
    #     while True:
    #         if not self.server_running or self.metrics_task.done():
    #             self.metrics_task.cancel()
    #             break
    #         time.sleep(0.1)
