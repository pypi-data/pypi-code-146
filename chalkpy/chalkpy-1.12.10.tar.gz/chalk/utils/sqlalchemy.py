import datetime
from typing import Optional, Union

from sqlalchemy import DateTime, TypeDecorator
from sqlalchemy.engine import Dialect


class UtcDateTime(TypeDecorator):
    """A timestamp, converted to UTC before DB insertion, optionally as a timezoned timestamp.

    The local orm value must be a :class:`datetime.datetime` with a the ``tzinfo`` set.

    Upon return from the database, the timezone of the python object will be converted to UTC.
    If the database does not store the timezone, then the raw value will be interpreted with the UTC timezone.
    (This should generally be a no-op, since we convert to UTC upon inserting into the database.)
    """

    impl = DateTime

    cache_ok = True

    def _format_datetime_as_iso(self, val: datetime.datetime):
        """Format a datetime as standardized ISO string, independent of platform"""
        # See https://bugs.python.org/issue13305 -- `datetime.datetime.min.isoformat()` is incorrect on linux
        # It returns 1-01-01T00:00:00 instead of 0001-01-01T00:00:00
        time_format = val.time().isoformat()
        return f"{val.year:04d}-{val.month:02d}-{val.day:02d}T{time_format}"

    def process_bind_param(
        self, value: Optional[Union[datetime.datetime, str]], dialect: Dialect
    ) -> Optional[Union[str, datetime.datetime]]:
        if value is not None:
            if isinstance(value, str) and dialect.name == "bigquery":
                if value.lower() in ("infinity", "inf", "+inf", "+infinity"):
                    value = datetime.datetime.max.replace(tzinfo=datetime.timezone.utc)
                elif value.lower() in ("-infinity", "-inf"):
                    value = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
            if isinstance(value, datetime.datetime):
                if value.tzinfo is None:
                    raise ValueError("unzoned datetime is disallowed")
                value = value.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                if dialect.name == "bigquery":
                    value = self._format_datetime_as_iso(value)
        return value

    def process_result_value(self, value: Optional[datetime.datetime], dialect: Dialect) -> Optional[datetime.datetime]:
        if value is not None:
            if not isinstance(value, datetime.datetime):
                raise TypeError(f"Unexpected datetime type: {type(value).__name__}")
            if value.tzinfo is not None:
                raise TypeError(f"DB datetime should not have a timezone")
            return value.replace(tzinfo=datetime.timezone.utc)
        return value

    def process_literal_param(self, value: Optional[Union[datetime.datetime, str]], dialect: Dialect) -> Optional[str]:
        # Need to override how to process a literal param, as the built-in SQLAlcehmy DateTime object
        # does not have a literal processor
        bind_value = self.bind_processor(dialect)(value)
        if bind_value is None:
            return "NULL"
        else:
            if isinstance(bind_value, datetime.datetime):
                bind_value = self._format_datetime_as_iso(bind_value)
            assert isinstance(bind_value, str)
            return f'"{bind_value}"'
