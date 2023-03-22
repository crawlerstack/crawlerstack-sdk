"""test datas"""
import base64

import pytest

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.utils.datas import check_data


@pytest.mark.parametrize(
    'data',
    [
        {
            'snapshot': True,
            'fields': ['file_name', 'content'],
            'datas': [['foo.pdf', 'foo']],
            'title': 'test'
        },
        {
            'snapshot': False,
            'fields': ['foo'],
            'datas': [['foo'], ['bar']],
            'title': 'test',
            'error': False
        },
        {
            'snapshot': False,
            'fields': ['foo'],
            'datas': [['foo', 'bar'], ['bar']],
            'title': 'test',
            'error': True
        },
    ]
)
def test_check_data(data):
    """test datas"""
    if data.get('snapshot'):
        # 存储为快照文件
        res = check_data(data=data, task_name='test', data_type='snapshot')
        file_data = base64.b64encode('foo'.encode('utf-8')).decode('utf-8')
        assert res == {'task_name': 'test',
                       'data': {
                           'title': 'test',
                           'snapshot_enabled': True,
                           'fields': ['file_name', 'content'],
                           'datas': [('foo.pdf', file_data)]
                       }}
    if data.get('error'):
        with pytest.raises(SpiderkeeperSdkException):
            check_data(data=data, task_name='test', data_type='data')
    if not data.get('snapshot') and not data.get('error'):
        res = check_data(data=data, task_name='test', data_type='data')
        assert res == {
            'data': {
                'datas': [['foo'], ['bar']],
                'fields': ['foo'],
                'snapshot_enabled': False,
                'title': 'test'
            },
            'task_name': 'test'}
