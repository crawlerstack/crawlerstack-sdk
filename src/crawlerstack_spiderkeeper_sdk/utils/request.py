"""request"""
import httpx
from requests import RequestException

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException
from crawlerstack_spiderkeeper_sdk.utils import SingletonMeta


class BaseReqeust(metaclass=SingletonMeta):
    """Base request"""
    NAME: str
    MAX_RETRY = 1


class BaseAsyncRequest(BaseReqeust):
    """Base async request"""

    async def request(self, *args, **kwargs):
        """request"""
        raise NotImplementedError


class RequestWithHttpx(BaseAsyncRequest):
    """Request with Httpx"""

    NAME = 'httpx'

    @staticmethod
    async def _request(method: str, url: str, **kwargs):
        """async request"""
        async with httpx.AsyncClient() as client:
            return await client.request(
                method=method,
                url=url,
                **kwargs
            )

    async def request(self, method: str, url: str, **kwargs):  # pylint: disable=arguments-differ
        """request"""
        try:
            for _ in range(self.MAX_RETRY):
                response = await self._request(method, url, **kwargs)
                if response.status_code != 200:
                    continue
                return response.json()
        except RequestException as ex:
            raise SpiderkeeperSdkException('Request failed.') from ex
