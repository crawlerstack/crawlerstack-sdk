# spiderkeeper-sdk

## Overview

spiderkeeper SDK

sdk 完成数据转发，数据校验，log 日志以及爬虫过程中监控指标的收集等功能
其中，监控作为后台任务由爬虫程序员控制其任务周期

## Installing

```bash
pip install crawlerstack-spiderkeeper-sdk
```

## Usage

- SDK 所需参数通过采集平台配置到环境变量中
- 将必要的 log 日志（例如异常等）通过 SDK 发送到采集平台，方便页面观察
- 其中，SDK 只将以 `spiderkeeper` 开头的指标发送带采集平台中

### Examples

为模拟真是数据转发，执行演示示例前，需要先将 api 服务开启 [start api server](tests/example/rest_api/server_start.py) 后通过日志输出观察

[示例代码](tests/example/main.py)

- 使用装饰器，设置每次请求的指标

```python
import functools

import httpx
from example.metrics import (exc_count, req_bytes, req_count,
                             req_method_count_GET, resp_bytes, resp_count,
                             resp_status_count_200, resp_status_count_301,
                             resp_status_count_302)
from requests import RequestException


def async_metrics(func):
    """async_metrics decorator"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        """
        set request metrics

        监控请求过程对应指标
        """
        req_count.inc()
        try:
            req_method_count_GET.inc()
            resp = await func(*args, **kwargs)
            status_code = resp.status_code
            resp_count.inc()
            req_bytes.inc(1.0)
            resp_bytes.inc(1.0)
            if status_code == 200:
                resp_status_count_200.inc()
                return resp
            if status_code == 302:
                resp_status_count_302.inc()
            if status_code == 301:
                resp_status_count_301.inc()
            return {}
        except RequestException as ex:
            exc_count.inc()
            raise ex

    return wrapper


class DemoRequest:
    """demo request"""
    client = httpx.AsyncClient(timeout=20)

    @async_metrics
    async def req_get(
            self,
            url: str,
            **kwargs
    ):
        """request get"""
        return await self.client.get(url=url, **kwargs)
```

- 爬虫示例

其中 SDK 收集监控指标的任务周期由爬虫程序控制

```python
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
            storage_enabled=self.enable(settings.STORAGE_ENABLE),
            snapshot_enabled=self.enable(settings.SNAPSHOT_ENABLE),
        )
        self.request = DemoRequest()

    @staticmethod
    def enable(config) -> bool:
        """
        Enable
        一些系统环境变量中的 bool类型参数表示为字符串,
        python中不可直接将其转化为bool类型,(在python中bool('')为 False ,bool('foo')为True)****
        :param config:
        :return:
        """
        if config in ('true', 'True') or config is True:
            return True
        if config in ('false', 'False') or config is False:
            return False
        return False

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
        # 爬虫结束后由爬虫程序关闭指标收集任务
        self.metrics_task.cancel()
        await asyncio.sleep(5)

    async def send_data(self, data):
        """send data"""
        await self.sdk.send_data(data=data)
```
