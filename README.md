# spiderkeeper-sdk

## Overview

spiderkeeper SDK

## Usage

- SDK 实例化时所需的参数通过采集平台配置到环境变量中
- 将必要的 log 日志（例如异常等）通过 SDK 发送到采集采集平台，方便页面观察
- 其中，采集平台只统计以下监控指标

```text
downloader_request_count
downloader_request_bytes
downloader_request_method_count_GET
downloader_response_count
downloader_response_status_count_200
downloader_response_status_count_301
downloader_response_status_count_302
downloader_response_bytes
downloader_exception_count
```

### Examples

- Monitor usage of request metrics

```python
import functools

import requests
from prometheus_client import Counter
from requests import RequestException

req_count = Counter('downloader_request_count', 'Number of requests')
req_bytes = Counter('downloader_request_bytes', 'Bytes of requests')
req_method_count_GET = Counter('downloader_request_method_count_GET', 'Number of GET requests')
resp_count = Counter('downloader_response_count', 'Number of responses')
resp_status_count_200 = Counter('downloader_response_status_count_200', 'Number of 200 responses')
resp_status_count_301 = Counter('downloader_response_status_count_301', 'Number of 301 responses')
resp_status_count_302 = Counter('downloader_response_status_count_302', 'Number of 302 responses')
resp_bytes = Counter('downloader_response_bytes', 'Bytes of responses')
exc_count = Counter('downloader_exception_count', 'Number of exceptions')


# 以上是采集平台所支持的监控指标


def metrics(func):
    """metrics decorator"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        set request metrics
        """
        req_count.inc()
        try:
            req_method_count_GET.inc()
            resp = func(*args, **kwargs)
            status_code = resp.status_code
            resp_count.inc()
            req_bytes.inc(len(resp.request.content))
            resp_bytes.inc(resp.num_bytes_downloaded)
            if status_code == 200:
                resp_status_count_200.inc()
                return resp
            if status_code == 302:
                resp_status_count_302.inc()
                return {}
            if status_code == 301:
                resp_status_count_301.inc()
                return {}
            return {}
        except RequestException as e:
            exc_count.inc()
            raise e

    return wrapper


class DemoRequest:
    """demo request"""

    @metrics
    def req_get(
            self,
            url: str,
            **kwargs
    ):
        """request get"""
        return requests.get(url=url, **kwargs)
```

- Usage in crawlers

```python
from tests.example.request import DemoRequest
from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from crawlerstack_spiderkeeper_sdk.config import settings

sdk = SpiderkeeperSDK(
    task_name=settings.TASK_NAME,
    data_url=settings.DATA_URL,
    log_url=settings.LOG_URL,
    metrics_url=settings.METRICS_URL,
    storage_enable=bool(settings.STORAGE_ENABLE),
    snapshot_enable=bool(settings.SNAPSHOT_ENABLE),
)


class DemoCrawlers:
    url = 'https://www.baidu.com/'
    request = DemoRequest()

    async def crawlers(self):
        """crawlers"""
        await sdk.logs(f'Crawler {self.url}')
        res = self.request.req_get(self.url)
        # 解析后的数据发送到采集平台中
        await self.send_data(res)

    @staticmethod
    async def send_data(data: dict):
        """send data"""
        await sdk.send_data(data=data)
```
