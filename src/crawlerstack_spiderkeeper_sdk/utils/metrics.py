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


def parse_metrics(data: dict) -> dict:
    """
    Parse metrics
    :param data:
    :return:
    """
    _kv = {}
    for family in text_string_to_metric_families(data):
        for sample in family.samples:
            name = sample.name
            if name.startswith(METRIC_PREFIX):
                try:
                    _kv.update({name.split('_total')[0]: int(sample.value)})
                except IndexError as ex:
                    raise SpiderkeeperSdkException(
                        'The metric name is incorrectly defined. '
                        'The metric data should be a string type prefixed with spiderkeeper'
                    ) from ex
                except TypeError as ex:
                    raise SpiderkeeperSdkException(
                        'The indicator data is set incorrectly. '
                        'The metric data should be a number of type int'
                    ) from ex
    return _kv

# ('xlsx', 'xls', 'pdf', 'doc', 'docs')
# base64.b64encode(data).decode('utf-8')
