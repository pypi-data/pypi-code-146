from datetime import datetime, MINYEAR


_dt_chars = ['y', 'M', 'd', 'h', 'm', 's']
_parse_format_chars = [
    'y', # Year
    'M', # Month
    'd', # Date
    'h', # Hour
    'm', # Minute
    's', # Second
    '*'  # Wildcard
]


class DateTimeParseFormatError(Exception):
    pass

class DateTimeParseError(Exception):
    pass


def parse_date(raw_date: str, parse_format = "yyyy-MM-dd") -> datetime:
    _validate_parse_format(parse_format)
    raw_date = _remove_extra_chars(raw_date, parse_format)

    dfields = _get_datetime_fields(raw_date, parse_format)
    now = datetime.now()

    year = now.year
    if 'y' in dfields:
        try:
            year = int(dfields.get('y'))
        except ValueError:
            raise DateTimeParseError(
                'Year must be a valid number. '\
                    f'raw_date: { raw_date } format: { parse_format }'
            )

    month = now.month
    if 'M' in dfields:
        try:
            month = int(dfields.get('M'))
        except ValueError:
            raise DateTimeParseError(
                'Month must be a valid number. '\
                    f'raw_date: { raw_date } format: { parse_format }'
            )

    day = now.day
    if 'd' in dfields:
        try:
            day = int(dfields.get('d'))
        except ValueError:
            raise DateTimeParseError(
                'Day must be a valid number. '\
                    f'raw_date: { raw_date } format: { parse_format }'
            )

    hour = 0
    if 'h' in dfields:
        try:
            hour = int(dfields.get('h'))
        except ValueError:
            raise DateTimeParseError(
                'Hour must be a valid number. '\
                    f'raw_date: { raw_date } format: { parse_format }'
            )

    minute = 0
    if 'm' in dfields:
        try:
            minute = int(dfields.get('m'))
        except ValueError:
            raise DateTimeParseError(
                'Minute must be a valid number. '\
                    f'raw_date: { raw_date } format: { parse_format }'
            )

    second = 0
    if 's' in dfields:
        try:
            second = int(dfields.get('s'))
        except ValueError:
            raise DateTimeParseError(
                'Seconds must be a valid number. '\
                    f'raw_date: { raw_date } format: { parse_format }'
            )

    return datetime(
        year,
        month,
        day,
        hour,
        minute,
        second
    )


def _get_datetime_fields(raw_date: str, parse_format = 'yyyy-mm-dd') -> dict:
    """Retrieves values for each datetime field from given raw date \
        using given parse format

    Args:
        raw_date (str): String representing/containing a datetime
        parse_format (str, optional): Format to use to parse raw_date. \
            Defaults to 'yyyy-mm-dd'.

    Returns:
        dict: Values for each datetime field (y, M, d, h, m, s)
    """

    # Chars covered by wildcard (*) where already removed from raw_date
    # so remove them from format for iteration
    parse_format = parse_format.strip('*')

    dt_parts = {}
    for idx, format_char in enumerate(parse_format):
        if format_char in _dt_chars:
            if format_char in dt_parts:
                dt_parts[format_char] += raw_date[idx]
            else:
                dt_parts[format_char] = raw_date[idx]

    return dt_parts


def _remove_extra_chars(raw_date: str, parse_format: str) -> str:
    """If parse format contains a '*' at begining or ending, will remove \
        characters covered by such '*' from raw date. e.g.: \
        Raw date: 'asdf2019-01-31', Parse format: '*yyyy-mm-dd' will result \
        into '2019-01-31'. \
        \
        Note: Make sure to invoke _validate_parse_format before this function

    Args:
        raw_date (str): String representing a datetime
        parse_format (str): Format to parse raw_date

    Returns:
        str: raw_date without chracters covered by '*'
    """
    if parse_format.startswith('*'):
        datetime_length = len(parse_format) - 1
        datetime_start = len(raw_date) - datetime_length

        return raw_date[datetime_start:]

    elif parse_format.endswith('*'):
        datetime_length = len(parse_format) - 1
        return raw_date[0:datetime_length]

    return raw_date


def _validate_parse_format(format: str) -> None:
    """Validates that given date format is valid for parsing strings as dates \
        or raises an InvalidDateParseFormatError exception

    Args:
        format (str): Datetime format to validate

    Raises:
        InvalidDateParseTimeFormatError: If given format is invalid
    """
    frequencies: dict = {}
    last_char: str = None

    for c in format:
        if c in ['y', 'M', 'd', 'h', 'm', 's']:

            # Increase frequency count for char
            freq = (frequencies.get(c) + 1) if c in frequencies else 1
            frequencies[c] = freq

            if freq > 1 and last_char != c:
                raise DateTimeParseFormatError(
                    f'Datetime formats with several "{ c }" chars ' \
                    'must have them contiguous'
                )
        last_char = c

    # Validate char frequencies per field
    for c, freq in frequencies.items():
        if c == '*':
            if freq > 1:
                raise DateTimeParseFormatError(
                    'Only one "*" is allowed in date time format'
                )

            if not format.startswith('*') and not format.endswith('*'):
                raise DateTimeParseFormatError(
                    '"*" char is only allowed at begining or ending of format'
                )

        elif c in ['M', 'd', 'h', 'm', 's'] and freq > 2:
            raise DateTimeParseFormatError(
                f'No more than two "{ c }" are allowed in datetime format'
            )

        elif c == 'y' and freq != 4:
            raise DateTimeParseFormatError(
                f'Four "y" digits are necessary for year parsing in format'
            )
