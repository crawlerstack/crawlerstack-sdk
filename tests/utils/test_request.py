"""test request"""
import pytest
from httpx import Response, RequestError

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.utils.request import (BaseAsyncRequest,
                                                         RequestWithHttpx)


@pytest.mark.asyncio
async def test_base_async_request():
    """test async request"""
    base_req = BaseAsyncRequest()
    with pytest.raises(NotImplementedError):
        await base_req.request()


@pytest.mark.asyncio
async def test_httpx_request(mocker):
    """test httpx request"""
    req = RequestWithHttpx()
    mocker.patch.object(RequestWithHttpx, '_request', return_value=Response(status_code=200, json='foo'))
    res = await req.request('GET', 'foo')
    assert res == 'foo'


@pytest.mark.asyncio
async def test_httpx_request_error(mocker):
    """test request exception"""
    req = RequestWithHttpx()
    mocker.patch.object(RequestWithHttpx, '_request', side_effect=RequestError('test'))
    with pytest.raises(SpiderkeeperSdkException):
        await req.request('GET', 'foo')
