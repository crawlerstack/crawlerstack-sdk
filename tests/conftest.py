"""Test config"""
import pytest

from crawlerstack_spiderkeeper_sdk.repeater import SpiderkeeperSDK
from tests.example.utils import DemoRequest


@pytest.fixture()
def sdk():
    """Fixture sdk"""
    yield SpiderkeeperSDK(
        task_name='test',
        data_url='foo',
        log_url='foo',
        metrics_url='foo',
        storage_enable=True,
    )


@pytest.fixture()
def req():
    """req"""
    yield DemoRequest()
