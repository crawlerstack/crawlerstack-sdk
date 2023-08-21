"""schemas"""
from typing import Any

from pydantic import BaseModel, constr  # pylint: disable=no-name-in-module


class LogSchema(BaseModel):
    """Log schema."""
    task_name: constr(max_length=200)
    data: list[str] | tuple[str]


class MetricSchema(BaseModel):
    """Metric schema."""
    task_name: constr(max_length=200)
    data: dict[str, Any]


class DataContentSchema(BaseModel):
    """Data content schema"""
    title: constr(max_length=200)
    snapshot_enabled: bool = False
    fields: list
    datas: list[tuple[Any] | list[Any]]


class DataSchema(BaseModel):
    """Data schema."""
    task_name: constr(max_length=200)
    data: DataContentSchema
