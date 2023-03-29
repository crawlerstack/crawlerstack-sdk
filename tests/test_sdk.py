"""test sdk"""

import pytest

from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from crawlerstack_spiderkeeper_sdk.utils.request import RequestWithHttpx


@pytest.mark.parametrize(
    'storage_enable,snapshot_enable',
    [
        (True, True),
        (False, False),
        (True, False)
    ]
)
@pytest.mark.asyncio
async def test_send_data(mocker, storage_enable, snapshot_enable):
    """test send data"""
    request_post = mocker.patch.object(RequestWithHttpx, 'request')
    data_type = 'data'
    data = {
        'snapshot': 'data',
        'title': 'test',
        'fields': ['foo'],
        'datas': [['foo'], ['bar']]
    }
    sdk = SpiderkeeperSDK(
        task_name='test', data_url='foo', log_url='foo', metrics_url='foo', storage_enabled=storage_enable,
        snapshot_enabled=snapshot_enable
    )
    if storage_enable and snapshot_enable:
        await sdk.send_data(data=data, data_type=data_type)
        request_post.assert_called_with(
            'POST', 'foo',
            json={'data': {'datas': [['foo'], ['bar']],
                           'fields': ['foo'],
                           'snapshot': 'data',
                           'snapshot_enabled': False,
                           'title': 'test'},
                  'task_name': 'test'})

    if not storage_enable:
        res = await sdk.send_data(data=data, data_type=data_type)
        assert res == 'Storage not enabled'
    if storage_enable and not snapshot_enable:
        res = await sdk.send_data(data=data, data_type='snapshot')
        assert res == 'Snapshot not enabled'


@pytest.mark.asyncio
async def test_logs(mocker, sdk):
    """test send logs"""
    request_post = mocker.patch.object(RequestWithHttpx, 'request')
    await sdk.send_log('foo')
    request_post.assert_called_with('POST', 'foo', json={'data': ['foo'], 'task_name': 'test'})
