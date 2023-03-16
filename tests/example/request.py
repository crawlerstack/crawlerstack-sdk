"""example request"""
import functools

import requests
from prometheus_client import Counter
from requests import RequestException

req_count = Counter('downloader_request_count', 'Number of requests')
req_bytes = Counter('downloader_request_bytes', 'Bytes of requests')
req_method_count_GET = Counter('downloader_request_method_count_GET', 'Number of GET requests')
resp_count = Counter('downloader_response_count', 'Number of responses')
resp_status_count_200 = Counter('downloader_response_status_count_200', 'Number of 200 responses')
resp_status_count_301 = Counter('downloader_response_status_count_301', 'Number of 301 responses')
resp_status_count_302 = Counter('downloader_response_status_count_302', 'Number of 302 responses')
resp_bytes = Counter('downloader_response_bytes', 'Bytes of responses')
exc_count = Counter('downloader_exception_count', 'Number of exceptions')


def metrics(func):
    """metrics decorator"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        set request metrics
        """
        req_count.inc()
        try:
            req_method_count_GET.inc()
            resp = func(*args, **kwargs)
            status_code = resp.status_code
            resp_count.inc()
            # req_bytes.inc(len(resp.request.content))
            req_bytes.inc(1.0)
            # resp_bytes.inc(resp.num_bytes_downloaded)
            resp_bytes.inc(1.0)
            if status_code == 200:
                resp_status_count_200.inc()
                return {
                    'snapshot_enabled': True,
                    'title': 'test',
                    'fields': ['test'],
                    'datas': [['foo'], ['bar']]
                }
            if status_code == 302:
                resp_status_count_302.inc()
                return {}
            if status_code == 301:
                resp_status_count_301.inc()
                return {}
            return {}
        except RequestException as e:
            exc_count.inc()
            raise e

    return wrapper


class DemoRequest:
    """demo request"""

    @metrics
    def req_get(
            self,
            url: str,
            **kwargs
    ):
        """request get"""
        return requests.get(url=url, timeout=3, **kwargs)
