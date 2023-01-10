import calendar
import datetime as dt
from typing import Tuple

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

__all__ = ['end_of_day', 'end_of_month', 'previous_date_range']


def end_of_day(date_):
    """
    >>> end_of_day(dt.datetime(2022, 1, 1, 11, 11))
    datetime.datetime(2022, 1, 1, 23, 59, 59)
    """
    if not isinstance(date_, dt.datetime):
        date_ = parse(date_)

    return dt.datetime.combine(date_.date(), dt.time(23, 59, 59))


def end_of_month(start_date: dt.date) -> dt.date:
    """
    >>> end_of_month(dt.date(2019, 2, 24))
    datetime.date(2019, 2, 28)
    """
    _, end_day = calendar.monthrange(start_date.year, start_date.month)
    return dt.date(start_date.year, start_date.month, end_day)


def previous_date_range(now: dt.date = None) -> Tuple[dt.date, dt.date]:
    """
    >>> previous_date_range(dt.date(2020, 11, 5))
    (datetime.date(2020, 10, 1), datetime.date(2020, 10, 31))
    >>> previous_date_range(dt.datetime(2020, 11, 5))
    (datetime.date(2020, 10, 1), datetime.date(2020, 10, 31))
    """
    now = now or dt.datetime.now()

    from_ = (now - relativedelta(months=1)).replace(day=1)
    if isinstance(from_, dt.datetime):
        from_ = from_.date()

    to = end_of_month(from_)

    return from_, to
