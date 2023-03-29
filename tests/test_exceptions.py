"""test exceptions"""
from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException


def test_exception():
    """test exception"""
    res = SpiderkeeperSdkException("test")
    assert res.message == "test"
