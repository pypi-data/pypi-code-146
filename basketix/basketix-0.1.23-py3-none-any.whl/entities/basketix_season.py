"""Week id module"""

from datetime import datetime
from typing import Type, List

from .date_helper import DateHelper

class BasketixSeason:
    """Basketix season"""

    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f'Basketix season: {self._value}'

    @property
    def id(self) -> str:
        """Returns Basketix season id"""

        return self._value

    @property
    def nba_id(self) -> str:
        """Returns NBA season id"""

        return self._value[0:4]

    @property
    def first_day(self) -> str:
        """Returns first day of a NBA season, the 1st August"""

        start_year, _ = self._value.split('-')

        return self.start_date(year=int(start_year))

    @property
    def last_day(self) -> str:
        """Returns last day of a NBA season"""

        start_year, end_year = self._value.split('-')

        return self.end_date(year=int(f'{start_year[:2]}{end_year}'))

    @property
    def days(self) -> List[str]:
        """Returns all season days (i.e days between first day and last day)"""

        days = []

        first_day_dt = DateHelper.parse(self.first_day)
        last_day_dt = DateHelper.parse(self.last_day)

        pointer = first_day_dt
        while pointer <= last_day_dt:
            iso_date = DateHelper.to_ISO_date(pointer)
            days.append(iso_date)
            pointer = DateHelper.parse_ISO_date(DateHelper.delta_days(iso_date, 1))

        return days

    def next(self, delta=1) -> 'BasketixSeason':
        """Returns next delta week"""

        return self.delta(delta=delta)

    def previous(self, delta=1) -> 'BasketixSeason':
        """Returns previous delta week"""

        return self.delta(delta=-delta)

    def delta(self, delta=1) -> 'BasketixSeason':
        """Returns delta season"""

        _datetime = DateHelper.parse(self.first_day)
        _datetime_delta = datetime(year=_datetime.year + delta, month=_datetime.month, day=_datetime.day)

        return self.from_date(_datetime_delta.strftime(DateHelper.DATE_ISO_FORMAT))

    @classmethod
    def from_date(cls: Type['BasketixSeason'], date: str) -> 'BasketixSeason':
        """Parse date and return Season instance"""

        _datetime = DateHelper.parse(date)

        season_limit_date = DateHelper.parse(cls.end_date(_datetime.year))

        if _datetime > season_limit_date:
            first_part = _datetime
            date_next_year = DateHelper.delta_days(date=date, days=365)
            _datetime_next_year = DateHelper.parse(date_next_year)
            second_part = _datetime_next_year
        else:
            second_part = _datetime
            date_last_year = DateHelper.delta_days(date=date, days=-365)
            _datetime_last_year = DateHelper.parse(date_last_year)
            first_part = _datetime_last_year

        return cls(value=f'{first_part.strftime("%Y")}-{second_part.strftime("%y")}')

    @classmethod
    def start_date(cls: Type['BasketixSeason'], year: int) -> str:
        """Return season start date, the 1st August"""

        return datetime(year=year, month=8, day=1).strftime(DateHelper.DATE_ISO_FORMAT)

    @classmethod
    def end_date(cls: Type['BasketixSeason'], year: int) -> str:
        """Return season end date, the 31st July"""

        return datetime(year=year, month=7, day=31).strftime(DateHelper.DATE_ISO_FORMAT)
