
import locale

locale.setlocale(locale.LC_ALL, '')


def format_datetime(value, fmt='%Y년 %m %d %H:%M'):
    return value.strftime(fmt)
