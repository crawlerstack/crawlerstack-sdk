"""test metrics"""
import pytest
from prometheus_client import REGISTRY, Counter, generate_latest

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.utils.metrics import (get_metrics,
                                                         parse_metrics)


@pytest.mark.parametrize(
    'exc',
    [
        True,
        False,
    ]
)
def test_get_metrics(mocker, exc):
    """test get metrics"""
    if not exc:
        mocker.patch(
            'crawlerstack_spiderkeeper_sdk.utils.metrics.parse_metrics',
            return_value='foo'
        )
        res = get_metrics()
        assert res == 'foo'
    else:
        mocker.patch(
            'crawlerstack_spiderkeeper_sdk.utils.metrics.parse_metrics',
            side_effect=SpiderkeeperSdkException('test')
        )
        res = get_metrics()
        assert not res


def test_parse_metrics():
    """test parse metrics"""
    test_metrics = Counter('spiderkeeper_test', 'test')
    test_metrics.inc()
    registry = REGISTRY
    data = generate_latest(registry).decode('utf-8')
    res = parse_metrics(['spiderkeeper_test'], data)
    assert res.get('spiderkeeper_test') == 1


def test_parse_metrics_non_int():
    """test parse metrics non int"""
    data = '# HELP spiderkeeper_test_total Number of 301 responses\n' \
           '# TYPE spiderkeeper_test_total counter\nspiderkeeper_test_total a\n' \
           '# HELP spiderkeeper_test_created Number of 301 responses\n' \
           '# TYPE spiderkeeper_test_created gauge\nspiderkeeper_test_created 1.679455739759572e+09\n'
    with pytest.raises(SpiderkeeperSdkException):
        parse_metrics([], data)
