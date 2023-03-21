"""datas"""
import base64
import os

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException

# ('xlsx', 'xls', 'pdf', 'doc', 'docs')
# base64.b64encode(data).decode('utf-8')
SNAPSHOT_TYPE = ('.xlsx', '.xls', '.pdf', '.doc', '.docs')


def check_data(data: dict, task_name: str, data_type: str):
    """
    Check if the data type is 'snapshot'.

    :param data:
    :param task_name:
    :param data_type:
    :return:
    """
    snapshot_data = []
    if data_type == 'snapshot':
        snapshot_enabled = True
        for file_name, file_data in data.get("datas", []):
            if os.path.splitext(file_name)[-1] in SNAPSHOT_TYPE:
                file_data = base64.b64encode(file_data.encode('utf-8')).decode('utf-8')
            snapshot_data.append((file_name, file_data))
    else:
        snapshot_enabled = False

    fields = data.get("fields", [])
    datas = data.get("datas", [])

    if not all(len(row) == len(fields) for row in datas):
        raise SpiderkeeperSdkException(
            'The field field length is not consistent with the data length'
        )

    return {
        'task_name': task_name,
        'data': {
            'title': data.get("title"),
            'snapshot_enabled': snapshot_enabled,
            'fields': fields,
            'datas': datas
        }
    }
