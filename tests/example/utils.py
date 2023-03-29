"""example request"""
import functools

import httpx
from httpx import RequestError

from .metrics import (exc_count, req_bytes, req_count, req_method_count_GET,
                      resp_bytes, resp_count, resp_status_count_200,
                      resp_status_count_301, resp_status_count_302)


def async_metrics(func):
    """async_metrics decorator"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        """
        set request metrics

        监控请求过程对应指标
        """
        req_count.inc()
        try:
            req_method_count_GET.inc()
            resp = await func(*args, **kwargs)
            status_code = resp.status_code
            resp_count.inc()
            req_bytes.inc(1.0)
            resp_bytes.inc(1.0)
            if status_code == 200:
                resp_status_count_200.inc()
                return resp
            if status_code == 302:
                resp_status_count_302.inc()
            if status_code == 301:
                resp_status_count_301.inc()
            return {}
        except RequestError as ex:
            exc_count.inc()
            raise ex

    return wrapper


class DemoRequest:
    """demo request"""
    client = httpx.AsyncClient(timeout=20)

    @async_metrics
    async def req_get(
            self,
            url: str,
            **kwargs
    ):
        """request get"""
        return await self.client.get(url=url, **kwargs)
