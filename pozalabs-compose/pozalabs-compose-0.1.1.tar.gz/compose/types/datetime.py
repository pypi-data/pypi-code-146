from __future__ import annotations

import datetime
from typing import Any, Callable, Generator, Union

import pendulum
from pendulum.tz.timezone import Timezone
from pydantic.datetime_parse import parse_datetime


class DateTime(pendulum.DateTime):
    @classmethod
    def __get_validators__(cls) -> Generator[Callable[[Any], DateTime], None, None]:
        yield parse_datetime
        yield cls._to_dt

    @classmethod
    def _to_dt(cls, v: Union[datetime.datetime, pendulum.DateTime]) -> DateTime:
        if isinstance(v, datetime.datetime):
            return cls.from_datetime(v)
        return v

    @classmethod
    def from_datetime(cls, dt: datetime.datetime, tz: Timezone = pendulum.UTC) -> DateTime:
        return pendulum.instance(dt=dt, tz=tz)
