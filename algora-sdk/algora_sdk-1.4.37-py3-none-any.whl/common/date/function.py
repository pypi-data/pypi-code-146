"""
Date and time functions.
"""
import calendar
from datetime import date, datetime, time
from functools import lru_cache
from typing import List, Union

import pandas as pd
import pytz
from pandas import to_datetime, bdate_range
from pandas_market_calendars import get_calendar

from algora.common.date import DayCountConvention, SECONDS_IN_DAY
from algora.common.type import Datetime


@lru_cache(10)
def seconds_in_year(day_count_convention: DayCountConvention) -> float:
    """
    Calculate number of seconds per year based on day count convention. LRU cache is used to have 4x performance.

    Args:
        day_count_convention (DayCountConvention): Day count convention to use in calculation

    Returns:
        float: Number of seconds per year based on day count convention
    """
    return SECONDS_IN_DAY * float(day_count_convention)


def date_to_timestamp(as_of_date: date) -> int:
    """
    Convert date to epoch timestamp in milliseconds.

    Args:
        as_of_date (date): Python date

    Returns:
        int: Epoch timestamp in milliseconds
    """
    return calendar.timegm(as_of_date.timetuple()) * 1000


def datetime_to_timestamp(dt: datetime) -> int:
    """
    Convert datetime to epoch timestamp in milliseconds.

    Args:
        dt (datetime): Python datetime

    Returns:
        int: Epoch timestamp in milliseconds
    """
    return calendar.timegm(dt.utctimetuple()) * 1000


def datetime_to_utc(dt: datetime) -> datetime:
    """
    Standardize datetime to UTC. Assume that datetime where `tzinfo=None` is already in UTC.

    Args:
        dt (datetime): Python datetime

    Returns:
        datetime: Python datetime with standardized UTC timezone (`tzinfo=None`)
    """
    # assume that datetime without timezone is already in UTC
    if dt.tzinfo is None:
        return dt
    return dt.astimezone(pytz.utc).replace(tzinfo=None)


def date_to_datetime(as_of_date: date, as_of_time: time = datetime.min.time()) -> datetime:
    """
    Convert date and optional time to datetime. NOTE: time should not contain a timezone or else offset may not be
    correct.

    Args:
        as_of_date (date): Python date
        as_of_time (time): Python time

    Returns:
        datetime: Python datetime
    """
    return datetime.combine(as_of_date, as_of_time)


def standardize_date_or_datetime(as_of_date: Datetime) -> datetime:
    """
    Convert Datetime (Union[date, datetime]) to standardized UTC datetime.

    Args:
        as_of_date (date): Datetime

    Returns:
        datetime: Python UTC datetime
    """
    if isinstance(as_of_date, datetime):
        return datetime_to_utc(as_of_date)

    return date_to_datetime(as_of_date)


def timestamp_to_datetime(timestamp: int) -> datetime:
    """
    Transform epoch timestamp in milliseconds to datetime.

    Args:
        timestamp (int): Epoch timestamp in milliseconds

    Returns:
        datetime: Python datetime
    """
    return datetime.fromtimestamp(timestamp / 1000)


def delta_t(start: Union[datetime, pd.Series],
            end: Union[datetime, pd.Series],
            day_count_convention: DayCountConvention = DayCountConvention.ACTUAL_365_2425) -> Union[float, pd.Series]:
    """
    Calculate time to expiration given start series and end series, as well as numeric day_count.

    Args:
        start (datetime): Start (report) datetime
        end (datetime): End datetime, e.g. expiration datetime
        day_count_convention (DayCountConvention): Day count convention. Defaults to ACTUAL/365.2425

    Returns:
        float: Delta in time
    """
    denominator = seconds_in_year(day_count_convention)

    start_utc = datetime_to_utc(start) if isinstance(start, datetime) else start
    end_utc = datetime_to_utc(end) if isinstance(end, datetime) else end

    if isinstance(start_utc, pd.Series) or isinstance(end_utc, pd.Series):
        return (end_utc - start_utc).dt.total_seconds() / denominator
    else:
        return (end_utc - start_utc).total_seconds() / denominator


def create_dates_between(start: date, end: date, frequency: str = 'B') -> List[date]:
    """
    Create dates between start and end date (inclusive). Frequency used to determine which days of the week are used.

    Args:
        start (date): Python date
        end (date): Python date
        frequency (str): Frequency for date range

    Returns:
        List[date]: List of dates
    """
    return [dt.date() for dt in to_datetime(bdate_range(start=start, end=end, freq=frequency).to_list())]


def create_market_dates_between(start: date, end: date, name: str = 'NYSE') -> List[date]:
    """
    Create dates between start and end date (inclusive) given exchange calendar.

    Args:
        start (date): Python date
        end (date): Python date
        name (str): Calendar name, such as 'NYSE'

    Returns:
        List[date]: List of dates
    """
    return [dt.date() for dt in
            to_datetime(get_calendar(name).schedule(start_date=start, end_date=end).index).to_list()]
