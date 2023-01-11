# Various utilities related to date handling

from datetime import date as Date
from datetime import datetime as DateTime
from datetime import timedelta as TimeDelta
import re
import functools

today = Date.today

FORMAT = re.compile(r'^(\d{4})(?:\-|\/)(\d{1,2})(?:\-|\/)(\d{1,2})$')

def absolute_date(info):
    if isinstance(info, Date):
        return info
    elif isinstance(info, tuple):
        return Date(*info)
    elif isinstance(info, str) and FORMAT.match(info):
        return Date(*(int(x) for x in FORMAT.match(info).groups()))
    raise RuntimeError("Invalid date %s" % info)


HANDLERS = []

def register(expression=r'(.*)'):
    compiled = re.compile(expression)
    def chain(func):
        @functools.wraps(func)
        def wrapper(string):
            match = compiled.match(string)
            if match:
                return func(today(), *match.groups())
        HANDLERS.append(wrapper)
        return wrapper
    return chain

def relative_date(value):
    value = value.lower()
    if isinstance(value, str):
        result = next(filter(None, (h(value) for h in HANDLERS)), None)
        if result:
            return result
    return absolute_date(value)

@register(r'today')
def match_today(today):
    return today

@register(r'tomorrow')
def match_tomorrow(today):
    return today + TimeDelta(1)

@register(r'^(\d+)\s+days?$')
def match_days(today, days):
    return today + TimeDelta(int(days))

@register(r'^(\d+)d$')
def match_d(today, days):
    return today + TimeDelta(int(days))

@register(r'^(\d{1,2})$')
def match_day_num(today, day):
    if today.day < int(day):
        return Date(today.year, today.month, int(day))
    else:
        year = today.year + (today.month // 12)
        month = (today.month % 12) + 1
        return Date(year, month, int(day))

@register(r'(\d{1,2})(?:\-|\/)(\d{1,2})$')
def match_month_day_num(today, month, day):
    if today < Date(today.year, int(month), int(day)):
        return Date(today.year, int(month), int(day))
    else:
        return Date(today.year + 1, int(month), int(day))

@register(r'^(mon?|tue?s?|wed?n?e?s?|thu?r?s?|fri?|sat?u?r?|sun?)(?:day)?$')
def match_weekday(today, weekday):
    index = ['mo','tu','we','th','fr','sa','su'].index(weekday[0:2])
    days = (6 - today.weekday() + index) % 7 + 1
    return today + TimeDelta(days)
