"""test sdk"""

import httpx
import pytest
from requests import RequestException

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK


@pytest.mark.asyncio
async def test_send_data(mocker, sdk):
    """test send data"""
    request_post = mocker.patch.object(SpiderkeeperSDK, 'request_post')
    data = {
        'snapshot': 'data',
        'title': 'test',
        'fields': ['foo'],
        'datas': [['foo'], ['bar']]
    }
    await sdk.send_data(data=data, data_type='data')
    request_post.assert_called_with(
        'foo', {'data': {'datas': [['foo'], ['bar']],
                         'fields': ['foo'],
                         'snapshot_enabled': False,
                         'title': 'test'},
                'task_name': 'test'})


@pytest.mark.asyncio
async def test_logs(mocker, sdk):
    """test send logs"""
    request_post = mocker.patch.object(SpiderkeeperSDK, 'request_post')
    await sdk.logs('foo')
    request_post.assert_called_with(url='foo', data={'data': ['foo'], 'task_name': 'test'})


@pytest.mark.parametrize(
    'exception',
    [
        True,
        False
    ]
)
@pytest.mark.asyncio
async def test_request_post(mocker, exception, sdk):
    """test request post"""
    if not exception:
        post = mocker.patch.object(httpx.AsyncClient, 'post')
        await sdk.request_post('foo', {'foo': 'bar'})
        post.assert_called_with(url='foo', json={'foo': 'bar'})
    else:
        mocker.patch.object(httpx.AsyncClient, 'post', side_effect=RequestException)
        with pytest.raises(SpiderkeeperSdkException):
            await sdk.request_post('foo', {'foo': 'bar'})
