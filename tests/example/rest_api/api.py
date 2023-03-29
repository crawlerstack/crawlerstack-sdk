"""Example api"""
from example.rest_api.schemas import DataSchema, LogSchema, MetricSchema
from fastapi import APIRouter

router = APIRouter()


@router.post('/datas')
def datas(data: DataSchema):
    """datas"""
    print('发送数据成功', data)
    return 'ok'


@router.post('/logs')
def logs(data: LogSchema):
    """logs"""
    print('日志收集成功', data)
    return 'ok'


@router.post('/metrics')
def metrics(data: MetricSchema):
    """metrics"""
    print('监控指标收集成功', data)
    return 'ok'


@router.get('/example')
def example():
    """example"""
    return {
        'snapshot_enabled': False,
        'title': 'example',
        'fields': ['example'],
        'datas': [['foo'], ['bar']]
    }
