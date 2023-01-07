import datetime, calendar, os

def readable_date_min(date):
    return date.strftime("%m/%d")

def readable_date(date):
    return date.strftime("%m/%d/%Y")

def readable_week_min(date):
    return f'Week {date.isocalendar()[1]}'

def readable_week(date):
    return f'{date.isocalendar()[0]} W{date.isocalendar()[1]}'    

def readable_week_and_date(date):
    date_str = readable_date_min(date)
    week_str = readable_week(date)

    return f'{week_str} - {date_str}'

def filename_date_min(date):
    return date.strftime("%m.%d")

def filename_date(date):
    return date.strftime("%Y.%m.%d")

def filename_week_min(date):
    return readable_week_min(date)

def filename_week(date):
    return readable_week(date)

def filename_week_and_date(date):
    date_str = filename_date_min(date)
    week_str = filename_week(date)
    return f'{week_str} - {date_str}'
