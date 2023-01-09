import calendar
import datetime
from dateutil.relativedelta import relativedelta


def get_first_day(date):
    return datetime.date(date.year, date.month, 1)


def get_last_day(date):
    return datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month)[1])


def subtract_months_for_date(date, months_to_subtract=0):
    return (date - relativedelta(months=months_to_subtract)).date()
