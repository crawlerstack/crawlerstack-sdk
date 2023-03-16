"""crawlers"""

from crawlerstack_spiderkeeper_sdk.config import settings
from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from tests.example.request import DemoRequest

sdk = SpiderkeeperSDK(
    task_name=settings.TASK_NAME,
    data_url=settings.DATA_URL,
    log_url=settings.LOG_URL,
    metrics_url=settings.METRICS_URL,
    storage_enable=bool(settings.STORAGE_ENABLE),
    snapshot_enable=bool(settings.SNAPSHOT_ENABLE),
)


class DemoCrawlers:
    """DemoCrawlers"""
    url = 'https://www.baidu.com/'
    request = DemoRequest()

    async def crawlers(self):
        """crawlers"""
        await sdk.logs(f'Crawler {self.url}')
        res = self.request.req_get(self.url)
        await self.send_data(res)

    @staticmethod
    async def send_data(data):
        """send data"""
        await sdk.send_data(data=data)
