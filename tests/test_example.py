"""test request"""
import pytest
from httpx import URL

from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK

from .example.crawlers import DemoCrawlers
from .example.utils import DemoRequest


@pytest.mark.asyncio
async def test_req_get():
    """test req_get"""
    url = 'https://www.baidu.com/'
    req = DemoRequest()
    res = await req.req_get(url)
    assert res.url == URL(url)


@pytest.mark.asyncio
async def test_crawlers(mocker):
    """test crawlers"""
    spider = DemoCrawlers()
    url = 'http://localhost:8000/api/v1/example'
    logs = mocker.patch.object(SpiderkeeperSDK, 'send_log')
    send_data = mocker.patch.object(DemoCrawlers, 'send_data')
    await spider.crawlers()
    logs.assert_called_with(f'Crawler {url}')
    send_data.assert_called_with({'datas': [['foo'], ['bar']],
                                  'fields': ['example'],
                                  'snapshot_enabled': False,
                                  'title': 'example'})


@pytest.mark.asyncio
async def test_send(mocker):
    """test send data"""
    spider = DemoCrawlers()
    send_data = mocker.patch.object(SpiderkeeperSDK, 'send_data')
    await spider.send_data('foo')
    send_data.assert_called_with(data='foo')
