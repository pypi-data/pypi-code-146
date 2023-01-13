from datetime import datetime, timedelta
import calendar, enum, holidays
from math import ceil
from typing import Any, List


# first day of a month
MONTH_FIRST_DAY = 1
# first month of a year
YEAR_FIRST_MONTH = 1
# Days per week
DAYS_PER_WEEK = 7

# weeks in a year
MAX_YEAR_WEEK_NO = 53
DEFAULT_YEAR_WEEK_NO = 52

# days of the week
SUNDAY = 6
THURSDAY = 3

# months
JANUARY = 1
DECEMBER = 12

# calendar used for certain operations
CALENDAR = calendar.Calendar()


# ---------------- Holidays -----------------------
# CorporateHolidays: Custom holidays for the company based off Canadian holidays
class CorporateHolidays(holidays.Canada):
    def _populate(self, year):
        holidays.Canada._populate(self, year)

        # Remove Easter Monday
        self.pop_named("Easter Monday")


HOLIDAYS = CorporateHolidays()

# ------------------------------------------------


class DateTools():
    # convert_date(val, none_on_error): Tries to convert 'val' to a date
    @classmethod
    def convert_date(cls, val: Any, none_on_error: bool = True) -> Any:
        if (isinstance(val, datetime)):
            return val.date()
        elif (none_on_error):
            return None
        else:
            return val

    # is_month_start(): Determines if 'date_time' is the start of a month
    @classmethod
    def is_month_start(cls, date_time: datetime) -> bool:
        return (date_time.day == MONTH_FIRST_DAY)


    # is_year_start(): Determines if 'date_time' is the start of a year
    @classmethod
    def is_year_start(cls, date_time: datetime) -> bool:
        return (date_time.month == YEAR_FIRST_MONTH and cls.is_month_start(date_time))


    # get_next_month(date_time): Retrieves the integer representation of the next
    #   month and year
    @classmethod
    def get_next_month(cls, date_time: datetime) -> List[int]:
        if (date_time.month < DECEMBER):
            return [(date_time.month + 1), date_time.year]
        else:
            return [1, date_time.year + 1]


    # get_month_weekdays(month, year): Retrieves all the weekdays in a month
    @classmethod
    def get_month_weekdays(cls, month: int, year: int) -> List[datetime]:
        result = []

        for week in CALENDAR.monthdayscalendar(year, month):
            for i, day in enumerate(week):
                # not this month's day or a weekend
                if (day == 0 or i >= 5):
                    continue
                # or some other control if desired...
                result.append(datetime(year, month, day))
        return result


    # week_of_month(date_time): Retrieves the week of the month from 'date_time'
    @classmethod
    def week_of_month(cls, date_time: datetime) -> int:
        first_day = date_time.replace(day=1)
        adjusted_day_of_month = date_time.day + first_day.weekday()

        return int(ceil(adjusted_day_of_month / DAYS_PER_WEEK))


    # week_of_year(date_time): retrieves the week of the year from 'date_time'
    @classmethod
    def week_of_year(cls, date_time: datetime) -> int:
        return int(date_time.strftime("%W"))


    # get_month_start(date_time): Retrieves the day at the start of the month for 'date_time'
    @classmethod
    def get_month_start(cls, date_time: datetime) -> int:
        return date_time.replace(day=1)


    # get_year_start(year): Retreives the starting date of a year
    @classmethod
    def get_year_start(cls, year: int) -> datetime:
        return datetime(year, JANUARY, 1)


    # get_month_end(date_time): Retrieves the day at the end of the month for 'date_time'
    @classmethod
    def get_month_end(cls, date_time: datetime) -> int:
        # overage to get days for next month
        next_month = date_time.replace(day=28) + timedelta(days=4)
        # subtract next month overage by the number of days exceeded to get the last day of the month
        return next_month - timedelta(days=next_month.day)


    # get_shortend_weekday(date_time): Retrieves the shortened week day display for
    #   'date_time'
    @classmethod
    def get_shortend_weekday(cls, date_time: datetime):
        weekday = date_time.weekday()
        if (weekday == THURSDAY):
            return "THURS"
        else:
            return (date_time.strftime("%a")).upper()


    # is_last_week_of_year(date_time): Determines if 'date_time' is part of the
    #   last week in its year
    @classmethod
    def is_last_week_of_year(cls, date_time: datetime) -> bool:
        week_no = cls.week_of_year(date_time)
        return bool(week_no == MAX_YEAR_WEEK_NO or week_no == DEFAULT_YEAR_WEEK_NO)



    # is_same_week(dt1, dt2): Determines if 'dt1' and 'dt2' are in the same week
    @classmethod
    def is_same_week(cls, dt1: datetime, dt2: datetime) -> bool:
        # week no. in the year
        week_of_year1 = cls.week_of_year(dt1)
        week_of_year2 = cls.week_of_year(dt2)

        # day of the week
        day_of_week1 = dt1.weekday()
        day_of_week2 = dt2.weekday()

        year_diff = dt1.year - dt2.year

        if ((not year_diff and week_of_year1 == week_of_year2) or
            (year_diff == 1 and not week_of_year1 and is_last_week_of_year(day_of_week2) and day_of_week2 != SUNDAY) or
            (year_diff == -1 and not week_of_year2 and is_last_week_of_year(day_of_week1) and day_of_week1 != SUNDAY)):
            return True
        else:
            return False


    # is_holiday(date_time): Determines if 'date_time' is a holiday
    @classmethod
    def is_holiday(cls, date_time: datetime):
        current_date = date_time.date()
        return current_date in HOLIDAYS
