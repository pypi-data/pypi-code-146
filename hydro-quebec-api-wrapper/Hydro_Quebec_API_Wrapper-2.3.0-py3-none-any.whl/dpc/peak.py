"""Class describing a period."""
import datetime

from hydroqc.timerange import TimeRange
from hydroqc.winter_credit.consts import DEFAULT_PRE_HEAT_DURATION, EST_TIMEZONE

__all__ = ["PreHeat", "Peak"]


class PreHeat(TimeRange):
    """This class describe a period object."""

    def __init__(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
    ):
        """Period constructor."""
        super().__init__(start_date, end_date, True)


class Peak(TimeRange):
    """This class describe a period object."""

    # preheat: PreHeat

    def __init__(
        self,
        start_date: datetime.datetime,
        end_date: datetime.datetime,
        preheat_duration: int = DEFAULT_PRE_HEAT_DURATION,
    ):
        """Period constructor."""
        self._start_date: datetime.datetime = start_date.astimezone(EST_TIMEZONE)
        self._end_date: datetime.datetime = end_date.astimezone(EST_TIMEZONE)
        self._preheat_duration: int = preheat_duration
        super().__init__(self.start_date, self.end_date, is_critical=True)

    @property
    def date(self) -> datetime.date:
        """Get the day, without time, of the peak."""
        return self._start_date.date()

    @property
    def preheat(self) -> PreHeat:
        """Get the preheat period of the peak."""
        preheat_start_date = self.start_date - datetime.timedelta(
            minutes=self._preheat_duration
        )
        return PreHeat(preheat_start_date, self.start_date)

    @property
    def start_date(self) -> datetime.datetime:
        """Get the start date of the peak."""
        return self._start_date

    @property
    def end_date(self) -> datetime.datetime:
        """Get the end date of the peak."""
        return self._end_date
