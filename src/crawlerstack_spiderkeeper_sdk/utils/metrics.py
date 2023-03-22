"""metrics"""
import logging

from prometheus_client import REGISTRY, generate_latest
from prometheus_client.parser import text_string_to_metric_families

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException

logger = logging.getLogger(__name__)

METRIC_PREFIX = 'spiderkeeper'


def get_metrics() -> dict:
    """
    get metrics
    获取环境中监控指标
    :return:
    """
    try:
        registry = REGISTRY
        data = parse_metrics(generate_latest(registry).decode('utf-8'))
        return data
    except SpiderkeeperSdkException:
        return {}


def parse_metrics(data) -> dict:
    """
    Parse metrics
    :param data:
    :return:
    """
    _metrics = {}
    try:
        for family in text_string_to_metric_families(data):
            for sample in family.samples:
                name = sample.name
                if not name.startswith(METRIC_PREFIX):
                    continue
                _metrics.update({name.split('_total')[0]: int(sample.value)})
    except ValueError:
        raise SpiderkeeperSdkException(
            'The current value is and cannot be converted to int. '
            'The metrics should be a value that can be converted to an int. '
        )
    return _metrics
