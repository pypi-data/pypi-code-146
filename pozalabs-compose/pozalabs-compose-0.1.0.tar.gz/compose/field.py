from typing import Callable, Optional

import pendulum
from pydantic import Field
from pydantic.fields import FieldInfo


class _IdField:
    def __call__(self, alias: Optional[str] = None, **kwargs) -> FieldInfo:
        return Field(alias=alias or "_id", **kwargs)


class _DatetimeField:
    def __call__(self, **kwargs) -> FieldInfo:
        return Field(default_factory=pendulum.DateTime.utcnow, **kwargs)


IdField: Callable[..., FieldInfo] = _IdField()
DateTimeField: Callable[..., FieldInfo] = _DatetimeField()
