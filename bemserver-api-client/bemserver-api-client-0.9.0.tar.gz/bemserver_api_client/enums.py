"""BEMServer API client enums"""
import enum


class DataFormat(enum.Enum):
    csv = "application/csv"
    json = "application/json"


class Aggregation(enum.Enum):
    avg = "avg"
    sum = "sum"
    min = "min"
    max = "max"
    count = "count"


class BucketWidthUnit(enum.Enum):
    second = "second"
    minute = "minute"
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"
    year = "year"


class EventLevel(enum.Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
