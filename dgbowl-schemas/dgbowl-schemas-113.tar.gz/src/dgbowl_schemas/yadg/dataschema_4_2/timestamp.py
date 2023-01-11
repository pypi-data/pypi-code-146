from pydantic import BaseModel, Extra
from typing import Optional


class TimestampSpec(BaseModel, extra=Extra.forbid):
    """Specification of the column index and string format of the timestamp."""

    index: Optional[int]
    format: Optional[str]


class Timestamp(BaseModel, extra=Extra.forbid):
    """Timestamp from a column containing a single timestamp string."""

    timestamp: TimestampSpec


class UTS(BaseModel, extra=Extra.forbid):
    """Timestamp from a column containing a Unix timestamp."""

    uts: TimestampSpec


class TimeDate(BaseModel, extra=Extra.forbid):
    """Timestamp from a separate date and/or time column."""

    date: Optional[TimestampSpec]
    time: Optional[TimestampSpec]
