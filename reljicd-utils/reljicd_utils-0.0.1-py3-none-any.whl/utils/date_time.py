from datetime import datetime
from typing import Optional


def str_to_timestamp(timestamp: str) -> datetime:
    return datetime.strptime(timestamp, '%d %B %Y')


def year_to_timestamp(year: int) -> datetime:
    return datetime.strptime(str(year), '%Y')


def str_to_datetime(datetime_str: str) -> Optional[datetime]:
    if datetime_str:
        try:
            return datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S+00:00')
        except ValueError:
            return datetime.strptime(datetime_str, '%Y-%m-%d')
    else:
        return None
