"""Test"""
from pathlib import Path

from crawlerstack_spiderkeeper_sdk.config import settings


def update_test_settings():
    """
    更新测试配置
    :return:
    """
    test_config_path = Path(__file__).parent
    settings.load_file(test_config_path / 'settings.yml')
    settings.load_file(test_config_path / 'settings.local.yml')


update_test_settings()
