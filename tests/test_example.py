"""test request"""
import pytest

from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from tests.example.crawlers import DemoCrawlers
from tests.example.request import DemoRequest


def test_req_get(req):
    """test req_get"""
    res = req.req_get('https://www.baidu.com/')
    assert res == {
        'datas': [['foo'], ['bar']],
        'fields': ['test'],
        'snapshot_enabled': True,
        'title': 'test'
    }


@pytest.mark.asyncio
async def test_crawlers(mocker, crawlers):
    """test crawlers"""
    logs = mocker.patch.object(SpiderkeeperSDK, 'logs')
    send_data = mocker.patch.object(DemoCrawlers, 'send_data')
    mocker.patch.object(DemoRequest, 'req_get', return_value='foo')
    await crawlers.crawlers()
    logs.assert_called_with('Crawler https://www.baidu.com/')
    send_data.assert_called_with('foo')


@pytest.mark.asyncio
async def test_send(mocker, crawlers):
    """test send data"""
    send_data = mocker.patch.object(SpiderkeeperSDK, 'send_data')
    await crawlers.send_data('foo')
    send_data.assert_called_with(data='foo')
