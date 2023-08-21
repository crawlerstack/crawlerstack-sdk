"""初始化 prometheus 监控指标"""
from prometheus_client import Counter

req_count = Counter(
    'spiderkeeper_downloader_request_count',
    'Number of requests'
)
req_bytes = Counter(
    'spiderkeeper_downloader_request_bytes',
    'Bytes of requests'
)
req_method_count_GET = Counter(
    'spiderkeeper_downloader_request_method_count_GET',
    'Number of GET requests'
)
resp_count = Counter(
    'spiderkeeper_downloader_response_count',
    'Number of responses'
)
resp_status_count_200 = Counter(
    'spiderkeeper_downloader_response_status_count_200',
    'Number of 200 responses'
)
resp_status_count_301 = Counter(
    'spiderkeeper_downloader_response_status_count_301',
    'Number of 301 responses'
)
resp_status_count_302 = Counter(
    'spiderkeeper_downloader_response_status_count_302',
    'Number of 302 responses'
)
resp_bytes = Counter(
    'spiderkeeper_downloader_response_bytes',
    'Bytes of responses'
)
exc_count = Counter(
    'spiderkeeper_downloader_exception_count',
    'Number of exceptions'
)
