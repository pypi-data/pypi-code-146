from datetime import date


def to_date(day, month, year):
    try:
        return date(day=int(day), month=int(month), year=int(year))
    except Exception as error:
        raise RuntimeError(error)


def starts_with(value: str, prefix):
    return value is not None and value.startswith(prefix)


def true_if_none(value):
    return value if isinstance(value, bool) else True


def to_boolean(value):
    return value if isinstance(value, bool) else False
