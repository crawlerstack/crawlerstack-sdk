"""test datas"""

import pytest

from crawlerstack_spiderkeeper_sdk.utils.datas import check_data


@pytest.mark.parametrize(
    'data',
    [
        {
            'fields': 'file_name',
            'datas': [['foo.pdf', 'foo'.encode('utf-8')]],
            'title': 'foo'
        },
        {
            'fields': ['test'],
            'datas': [['foo']],
        },
        {
            'fields': ['test'],
            'datas': [['foo', 'bar']],
            'title': 'foo'
        },
        {
            'snapshot_enabled': True,
            'fields': ['file_name', 'content'],
            'datas': [['foo.pdf', 'foo'.encode('utf-8')]],
            'title': 'test'
        },
    ]
)
def test_check_data(data):
    """test datas"""
    #  check data type
    if not isinstance(data.get('fields'), (list, tuple)):
        with pytest.raises(ValueError):
            check_data(data=data, task_name='test')
    # Check if title has a value
    if not data.get('title'):
        with pytest.raises(ValueError):
            check_data(data=data, task_name='test')
    # Check the length of datas and fields
    if not all(len(row) == len(data.get('fields')) for row in data.get('datas')):
        with pytest.raises(ValueError):
            check_data(data=data, task_name='test')
    # Check snapshot data
    if data.get('snapshot_enabled'):
        res = check_data(data=data, task_name='test')
        assert res == {'data': {'datas': [('foo.pdf', 'Zm9v')],
                                'fields': ['file_name', 'content'],
                                'snapshot_enabled': True,
                                'title': 'test'},
                       'task_name': 'test'}
