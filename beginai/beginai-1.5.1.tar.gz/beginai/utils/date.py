from datetime import datetime


def parse_date_to_format(date: str, format='%d-%m-%Y'):
    return datetime.strptime(date, format).strftime(format)
