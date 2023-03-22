"""datas"""
import base64
import os

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException

SNAPSHOT_TYPE = ('.xlsx', '.xls', '.pdf', '.doc', '.docs')


def check_data(data: dict, task_name: str, data_type: str):
    """
    数据校验

    判断来源数据的存储方式，snapshot 形式存储则判断快照文件格式，以保证返回可保存的文件数据
    最后将符合格式要求的数据返回
    :param data:
    :param task_name:
    :param data_type:
    :return:
    """
    fields = data.get("fields", [])
    datas = data.get("datas", [])
    snapshot_data = []
    if data_type == 'snapshot':
        snapshot_enabled = True
        for file_name, file_data in data.get("datas", []):
            if os.path.splitext(file_name)[-1] in SNAPSHOT_TYPE:
                file_data = base64.b64encode(file_data.encode('utf-8')).decode('utf-8')
            snapshot_data.append((file_name, file_data))
        datas = snapshot_data
    else:
        snapshot_enabled = False

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
