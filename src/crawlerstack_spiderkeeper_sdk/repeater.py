"""repeater"""
import asyncio
import logging

import httpx
from requests import RequestException

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.utils.datas import check_data
from crawlerstack_spiderkeeper_sdk.utils.metrics import get_metrics

logger = logging.getLogger(__name__)


class SpiderkeeperSDK:
    """repeater"""
    client = httpx.AsyncClient(timeout=20)
    MAX_RETRY = 1
    metrics_data = {}

    def __init__(
            self,
            task_name: str,
            data_url: str,
            log_url: str,
            metrics_url: str,
            storage_enable=False,
            snapshot_enable=False
    ):
        self.metrics_task = None
        self.task_name: str = task_name
        self.log_url: str = log_url
        self.data_url: str = data_url
        self.metrics_url: str = metrics_url
        self.storage_enable = storage_enable
        self.snapshot_enable = snapshot_enable
        self._should_exit: bool = False

    async def send_data(self, data: dict, data_type: str = 'data'):
        """
        发送数据

        接口接收到的数据参数中fields与datas长度应保持一致
        :param data_type: 选择传入数据保存方式 `data`表示需要写入数据库的数据 `snapshot`表示需要保存为快照的文件数据
        :param data:
        :return:
        """
        if self.storage_enable:
            _data = check_data(data=data, task_name=self.task_name, data_type=data_type)
            if _data:
                await self.request_post(self.data_url, _data)

    async def logs(self, log: str):
        """
        logs

        上传必要的 log 日志信息
        :param log:
        :return:
        """
        data = {
            'task_name': self.task_name,
            'data': [log]
        }
        await self.request_post(url=self.log_url, data=data)

    async def metrics(self):
        """
        监控指标上传

        由 SDK 程序自行获取所需指标，并将时间周期内指标上传
        :return:
        """
        while 1:
            try:
                data = get_metrics()
            except SpiderkeeperSdkException:
                break
            _req_data = {}
            for item in data:
                _add_count = data.get(item) - self.metrics_data.get(item, 0)
                if _add_count > 0:
                    _req_data.update({item: _add_count})
            try:
                await self.request_post(url=self.metrics_url, data={
                    'task_name': self.task_name,
                    'data': _req_data
                })
            except SpiderkeeperSdkException:
                continue
            else:
                self.metrics_data = data
            await asyncio.sleep(5)

    async def request_post(self, url: str, data: dict):
        """
        request post
        :param url:
        :param data:
        :return:
        """
        for _ in range(self.MAX_RETRY):
            try:
                response = await self.client.post(url=url, json=data)
                if response.status_code != 200:
                    continue
                break
            except RequestException as ex:
                raise SpiderkeeperSdkException('Request failed.') from ex
