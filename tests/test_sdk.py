"""test sdk"""
import asyncio
import logging

import httpx
import pytest
from prometheus_client import REGISTRY, generate_latest
from requests import RequestException

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from crawlerstack_spiderkeeper_sdk.utils.metrics import parse_metrics
from tests.example.utils import resp_status_count_302


@pytest.mark.parametrize(
    'exc',
    [
        True,
        False,
    ]
)
def test_init_metrics_task(mocker, sdk, exc):
    """test init_metrics_task"""
    if exc:
        mocker.patch.object(SpiderkeeperSDK, 'metrics', side_effect=AttributeError)
        with pytest.raises(SpiderkeeperSdkException):
            sdk.init_metrics_task()
    else:
        create_task = mocker.patch.object(asyncio, 'create_task')
        sdk.init_metrics_task()
        create_task.assert_called()


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


@pytest.mark.parametrize(
    'check_data',
    [
        None,
        {'title': 'foo', 'fields': [], 'datas': [], 'snapshot_enabled': True}
    ]
)
def test_data(check_data, sdk):
    """test data"""
    if check_data:
        res = sdk.data(check_data)
        assert res == {
            'data': {'datas': [], 'fields': [], 'snapshot_enabled': True, 'title': 'foo'},
            'task_name': 'test'}
    else:
        assert sdk.data(
            {'title': 'foo', 'fields': [], 'datas': [[1, 2]], 'snapshot_enabled': True}
        ) is None


@pytest.mark.parametrize(
    'datas,fields',
    [
        ([], []),
        ([[1, 2]], [[]])
    ]
)
def test_check_data(datas, fields, sdk):
    """test check data"""
    if datas == fields:
        res = sdk.check_data(fields=fields, datas=datas)
        assert res
    elif datas != fields:
        res = sdk.check_data(fields=fields, datas=datas)
        assert not res


@pytest.mark.parametrize(
    'parser_metrics',
    [
        True,
        False
    ]
)
def test_get_metrics(mocker, parser_metrics, caplog, sdk):
    """test get metrics"""
    if parser_metrics:
        parser_metrics = mocker.patch.object(SpiderkeeperSDK, 'parser_metrics')
        sdk.get_metrics()
        parser_metrics.assert_called()
    else:
        mocker.patch.object(SpiderkeeperSDK, 'parser_metrics', side_effect=TypeError)
        caplog.set_level(logging.WARNING)
        sdk.get_metrics()
        assert 'WARNING' in caplog.text
        assert sdk._should_exit is True  # pylint: disable=protected-access


def test_parser_metrics():
    """test parser metrics"""
    resp_status_count_302.inc()
    data = generate_latest(REGISTRY).decode('utf-8')
    res = parse_metrics(data)
    assert res.get('downloader_response_status_count_302') == 1
