"""metrics"""
import logging

from prometheus_client import REGISTRY, generate_latest
from prometheus_client.parser import text_string_to_metric_families

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException

logger = logging.getLogger(__name__)

METRIC_PREFIX = 'spiderkeeper'
SUFFIX = ('sum', 'count', 'created', 'bucket')
registry = REGISTRY


def get_metrics() -> dict:
    """
    get metrics
    获取环境中监控指标
    :return:
    """
    try:
        collection = get_metrics_collection()
        data = generate_latest(registry).decode('utf-8')
        return parse_metrics(collection=collection, data=data)
    except SpiderkeeperSdkException:
        return {}


def get_metrics_collection():
    """
    get metrics collection
    :return:
    """
    res = []
    collection = registry.collect()
    for i in collection:
        name = i.name
        if name.startswith(METRIC_PREFIX):
            res.append(name)
    return res


def parse_metrics(collection: list, data: dict) -> dict:
    """
    Parse metrics
    :param collection:
    :param data:
    :return:
    """
    _metrics = {}
    try:
        for family in text_string_to_metric_families(data):
            for sample in family.samples:
                name = sample.name
                _metric_name = name.split('_total')[0]
                if _metric_name not in collection:
                    continue
                if name.startswith(METRIC_PREFIX) and name.split('_')[-1] in SUFFIX:
                    continue
                _metrics[_metric_name] = int(sample.value)
    except ValueError:
        raise SpiderkeeperSdkException(
            'The current value is and cannot be converted to int. '
            'The metrics should be a value that can be converted to an int. '
        )
    return _metrics
