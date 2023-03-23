"""datas"""


def check_data(data: dict, task_name: str):
    """
    数据校验

    判断来源数据的存储方式，snapshot 形式存储则判断快照文件格式，以保证返回可保存的文件数据
    最后将符合格式要求的数据返回
    :param data:
    :param task_name:
    :return:
    """
    fields = data.get("fields")
    datas = data.get("datas")
    if not all([
        isinstance(fields, (list, tuple)),
        task_name,
        isinstance(datas, (list, tuple)),
    ]):
        raise ValueError('Datas and fields must be a tuple or a list. A valid task_name should be passed in.')

    if not data.get('title'):
        raise ValueError('The data must contain the title value')

    fields_length = len(fields)
    if not all(len(row) == fields_length for row in datas):
        raise ValueError('Data validation failed. The field field length is not consistent with the data length.')

    return {
        'task_name': task_name,
        'data': data
    }
