"""repeater"""
import asyncio
import logging

import httpx
from prometheus_client import REGISTRY, generate_latest
from prometheus_client.parser import text_string_to_metric_families

from crawlerstack_spiderkeeper_sdk.constant import metric_name

logger = logging.getLogger(__name__)


class SpiderkeeperSDK:  # pylint: disable=too-many-instance-attributes
    """repeater"""
    client = httpx.AsyncClient(timeout=20)
    MAX_RETRY = 1
    metrics_data = {
        'downloader_request_count': 0,
        'downloader_request_bytes': 0,
        'downloader_request_method_count_GET': 0,
        'downloader_response_count': 0,
        'downloader_response_status_count_200': 0,
        'downloader_response_status_count_301': 0,
        'downloader_response_status_count_302': 0,
        'downloader_response_bytes': 0,
        'downloader_exception_count': 0
    }

    def __init__(
            self,
            task_name: str,
            data_url: str,
            log_url: str,
            metrics_url: str,
            storage_enable=False,
            snapshot_enable=False
    ):
        self.task_name: str = task_name
        self.log_url: str = log_url
        self.data_url: str = data_url
        self.metrics_url: str = metrics_url
        self.storage_enable = storage_enable
        self.snapshot_enable = snapshot_enable
        self._should_exit: bool = False

    async def send_data(self, data: dict):
        """
        发送数据
        接口接收到的数据参数中fields与datas长度应保持一致
        其中数据的 fields 与 datas 长度补不一致，则认为数据不完整，不进行数据发送
        :param data:
        :return:
        """
        _data = self.data(data)
        if self.storage_enable:
            if _data:
                await self.request_post(self.data_url, _data)

    def data(self, data: dict):
        """
        send data

        负责校验数据，如果校验失败则跳过不转发
        :param data:
        :return:
        """
        _snapshot_enabled = bool(data.get("snapshot_enabled", False))
        _title = data.get("title", None)
        _fields = data.get("fields", None)
        _datas = data.get("datas", None)
        if self.check_data(_fields, _datas):
            return {
                'task_name': self.task_name,
                'data': {
                    'title': data.get('title'),
                    'snapshot_enabled': _snapshot_enabled,
                    'fields': _fields,
                    'datas': _datas
                }
            }
        return None
        # 数据不符合要求时

    @staticmethod
    def check_data(fields: list, datas: list):
        """
        check data
        Check if the field is the same length as the data
        :param fields:
        :param datas:
        :return:
        """
        for data in datas:
            if len(data) != len(fields):
                return False
        return True

    async def logs(self, log: str):
        """
        logs

        上传 log 日志信息
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
        Upload metrics
        :return:
        """
        while not self._should_exit:
            await asyncio.sleep(15)
            data = self.get_metrics()
            for item in data:
                try:
                    _value = int(data.get(item))
                    _count = _value - int(self.metrics_data.get(item, 0))
                    if _count > 0:
                        self.metrics_data.update({item: _count})
                except Exception as e:  # pylint: disable=broad-except
                    logger.warning(e)
            await self.request_post(url=self.metrics_url, data={
                'task_name': self.task_name,
                'data': self.metrics_data
            })

    def get_metrics(self):
        """
        获取环境中监控指标
        """
        try:
            registry = REGISTRY
            data = self.parser_metrics(generate_latest(registry).decode('utf-8'))
            return data
        except Exception as e:  # pylint: disable=broad-except
            logger.warning(e)
            self._should_exit = True
        return None

    @staticmethod
    def parser_metrics(data: str):
        """
        Parser metrics
        从监控指标中解析出采集平台需要的部分
        :param data:
        :return:
        """
        _kv = {}
        for family in text_string_to_metric_families(data):
            for sample in family.samples:
                name = sample.name.split('_total')[0]
                if name in metric_name:
                    _kv.update({sample.name.split('_total')[0]: sample.value})
        return _kv

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
            except Exception as e:
                raise e
