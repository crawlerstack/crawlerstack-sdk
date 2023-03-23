"""crawlers"""
import asyncio

from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from . import settings
from .utils import DemoRequest


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
            storage_enabled=bool(settings.STORAGE_ENABLE),
            snapshot_enabled=bool(settings.SNAPSHOT_ENABLE),
        )
        self.request = DemoRequest()

    def init_metrics_collector_task(self):
        """
        由爬虫程序初始化监控指标收集任务
        :return:
        """
        self.metrics_task = asyncio.create_task(self.sdk.send_metrics())

    async def crawlers(self):
        """crawlers"""
        # 发送日志
        await self.sdk.send_log(f'Crawler {self.url}')
        await asyncio.sleep(1)
        res = await self.request.req_get(self.url)
        self.init_metrics_collector_task()
        # 发送数据
        await self.send_data(res.json())
        self.metrics_task.cancel()

    async def send_data(self, data):
        """send data"""
        await self.sdk.send_data(data=data)
