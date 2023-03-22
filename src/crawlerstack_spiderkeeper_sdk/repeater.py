"""repeater"""
import asyncio
import logging

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.utils.datas import check_data
from crawlerstack_spiderkeeper_sdk.utils.metrics import get_metrics
from crawlerstack_spiderkeeper_sdk.utils.request import RequestWithHttpx

logger = logging.getLogger(__name__)


class SpiderkeeperSDK:
    """repeater"""
    MAX_RETRY = 1
    metrics_data = {}

    def __init__(
            self,
            task_name: str,
            data_url: str,
            log_url: str,
            metrics_url: str,
            storage_enabled=False,
            snapshot_enabled=False
    ):
        self.metrics_task = None
        self.task_name: str = task_name
        self.log_url: str = log_url
        self.data_url: str = data_url
        self.metrics_url: str = metrics_url
        self.storage_enabled = storage_enabled
        self.snapshot_enabled = snapshot_enabled
        self._should_exit: bool = False
        self.request = RequestWithHttpx()

    async def send_data(self, data: dict, data_type: str = 'data'):
        """
        发送数据

        接口接收到的数据参数中fields与datas长度应保持一致
        :param data_type: 选择传入数据保存方式 `data`表示需要写入数据库的数据 `snapshot`表示需要保存为快照的文件数据
        :param data:
        :return:
        """
        if data_type == 'data':
            if self.storage_enabled:
                data.setdefault('snapshot_enabled', False)
            else:
                return 'Storage not enabled'
        elif data_type == 'snapshot':
            if self.snapshot_enabled:
                data.setdefault('snapshot_enabled', True)
            else:
                return 'Snapshot not enabled'

        _data = check_data(data=data, task_name=self.task_name)
        if _data:
            return await self.request.request('POST', self.data_url, json=_data)

    async def send_log(self, log: str):
        """
        send_log

        上传必要的 log 日志信息
        :param log:
        :return:
        """
        data = {
            'task_name': self.task_name,
            'data': [log]
        }
        return await self.request.request('POST', self.log_url, json=data)

    async def send_metrics(self):
        """
        监控指标上传

        由 SDK 程序自行获取所需指标，并将时间周期内指标上传
        :return:
        """
        while 1:
            await asyncio.sleep(5)
            try:
                data = get_metrics()
            except SpiderkeeperSdkException:
                break
            _req_data = {}
            for item in data:
                _add_count = data.get(item) - self.metrics_data.get(item, 0)
                if _add_count > 0:
                    _req_data.update({item: _add_count})
            if not _req_data:
                continue
            try:
                resp = await self.request.request('POST', self.metrics_url, json={
                    'task_name': self.task_name,
                    'data': _req_data
                })
                if not resp:
                    raise SpiderkeeperSdkException('Response failed')
            except SpiderkeeperSdkException:
                continue
            else:
                self.metrics_data = data
