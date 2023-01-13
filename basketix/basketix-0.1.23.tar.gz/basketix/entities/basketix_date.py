"""Date entity"""

from typing import Type

from .date_helper import DateHelper
from .basketix_week import BasketixWeek
from .basketix_season import BasketixSeason

class BasketixDate:
    """Basketix date"""

    def __init__(self, date: str, week: BasketixWeek, season: BasketixSeason) -> None:
        self.date = date
        self.week = week
        self.season = season

    def __repr__(self) -> str:
        return f'Basketix date: {self.date}'

    def __eq__(self, other):
        if isinstance(other, BasketixDate):
            return self.date == other.date

        return self.date == other

    @property
    def day_before(self) -> 'BasketixDate':
        """Returns day before"""

        return self.delta(delta=-1)

    @property
    def day_after(self) -> 'BasketixDate':
        """Returns day before"""

        return self.delta(delta=1)

    def delta(self, delta: int) -> 'BasketixDate':
        """Adding delta to the Basketix date"""

        return self.parse(DateHelper.delta_days(date=self.date, days=delta))

    @classmethod
    def today(cls: Type['BasketixDate']) -> 'BasketixDate':
        """Returns today Basketix date based on now"""

        return cls.parse(DateHelper.now())

    @classmethod
    def yesterday(cls: Type['BasketixDate']) -> 'BasketixDate':
        """Returns yesterday Basketix date based on now"""

        today = cls.today()

        return today.day_before

    @classmethod
    def tomorrow(cls: Type['BasketixDate']) -> 'BasketixDate':
        """Returns tomorrow Basketix date based on now"""

        today = cls.today()

        return today.day_after

    @classmethod
    def parse(cls: Type['BasketixDate'], date: str) -> 'BasketixDate':
        """Parses date and returns BasketixDate instance"""

        _datetime = DateHelper.parse(date)
        if _datetime.tzinfo:
            _datetime = _datetime.astimezone(DateHelper.US_EASTERN_TIMEZONE)
        elif  len(date) > 10 and not _datetime.tzinfo:
            _datetime = _datetime.astimezone(DateHelper.UTC).astimezone(DateHelper.US_EASTERN_TIMEZONE)

        formatted_date = _datetime.strftime(DateHelper.DATE_ISO_FORMAT)

        return cls(
            date=formatted_date,
            week=BasketixWeek.from_date(formatted_date),
            season=BasketixSeason.from_date(formatted_date),
        )
