"""Date helper"""

from datetime import datetime, timedelta
from typing import Type

from dateutil.parser import parse
from dateutil import tz
from pytz import utc

class DateHelper:
    """Date helper class"""

    US_EASTERN_TIMEZONE = tz.gettz('US/Eastern')
    DATE_ISO_FORMAT = '%Y-%m-%d'
    UTC = utc

    @classmethod
    def now(cls: Type['DateHelper']) -> str:
        """Returns ISO-formatted now"""

        return datetime.now().astimezone(utc).isoformat()

    @classmethod
    def delta_days(cls: Type['DateHelper'], date: str, days: int) -> str:
        """Returns date + delta ISO-formatted date"""

        _date = cls.parse_ISO_date(date)
        new_date = _date + timedelta(days=days)

        return cls.to_ISO_date(new_date)

    @classmethod
    def parse(cls: Type['DateHelper'], datetime_str: str) -> datetime:
        """Parses datetime"""

        return parse(datetime_str)

    @classmethod
    def to_ISO_date(cls: Type['DateHelper'], date: datetime) -> str:
        """Returns ISO-formatted date"""

        return date.strftime(cls.DATE_ISO_FORMAT)

    @classmethod
    def parse_ISO_date(cls: Type['DateHelper'], date: str) -> datetime:
        """Parses ISO-formatted date and returns datetime object"""

        return datetime.strptime(date, cls.DATE_ISO_FORMAT)

