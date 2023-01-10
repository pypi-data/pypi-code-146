"""This Module stores utils for pretty printing Datetime objects"""
from datetime import datetime

from dateutil import tz


def get_human_readable_date(
        dt: datetime,
        *,
        to_tz=tz.tzlocal(),
) -> str:
    """Parses a datetime string into friendly readable form

        Args:
            dt: Datetime string to parse
            to_tz: Timezone to return the string in
                By default, return in the local timezone

        Returns:
            Formatted datetime string in specified timezone
    """
    if not dt.tzinfo:
        from_tz = tz.UTC
        dt = dt.replace(tzinfo=from_tz)

    dt_in_tz = dt.astimezone(to_tz)

    dt_formatted: str = f'{dt_in_tz:%Y-%m-%d %I:%M%p}'
    return dt_formatted
