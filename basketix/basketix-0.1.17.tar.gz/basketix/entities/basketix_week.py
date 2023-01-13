"""Week id module"""

from typing import List, Type
from datetime import datetime

from isoweek import Week

from .date_helper import DateHelper
from .basketix_season import BasketixSeason

class BasketixWeek:
    """Basketix week class"""

    SEPARATOR = '_'

    def __init__(self, value: str) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f'Basketix week: {self._value}'

    @property
    def id(self) -> str:
        """Returns week id"""

        return self._value

    @property
    def year(self) -> int:
        """Returns week year"""

        return int(self._value.split(self.SEPARATOR)[0])

    @property
    def week_number(self) -> int:
        """Returns week number"""

        return int(self._value.split(self.SEPARATOR)[1])

    @property
    def days(self) -> List[str]:
        """Returns all days of a week."""

        return [day.strftime(DateHelper.DATE_ISO_FORMAT) for day in Week(self.year, self.week_number).days()]

    @property
    def first_day(self) -> str:
        """Returns first days of a week as string"""

        return self.days[0]

    @property
    def last_day(self) -> str:
        """Returns last days of a week as string"""

        return self.days[-1]

    @property
    def season(self) -> 'BasketixSeason':
        """Returns all days of a week."""

        first_day_of_week = self.days[0]

        return BasketixSeason.from_date(first_day_of_week)

    def next(self, delta=1) -> 'BasketixWeek':
        """Returns next delta week"""

        date = DateHelper.delta_days(self.first_day, days=7*delta)

        return self.from_date(date=date)

    def previous(self, delta=1) -> 'BasketixWeek':
        """Returns previous delta week"""

        date = DateHelper.delta_days(self.first_day, days=-7*delta)

        return self.from_date(date=date)

    @classmethod
    def from_date(cls: Type['BasketixWeek'], date: str) -> 'BasketixWeek':
        """Parses date and returns Week instance"""

        parse_date = datetime.strptime(date, DateHelper.DATE_ISO_FORMAT)
        year, week_number, _ = parse_date.isocalendar()

        week_id = f'{year}_{week_number:02d}'

        return cls(value=week_id)
