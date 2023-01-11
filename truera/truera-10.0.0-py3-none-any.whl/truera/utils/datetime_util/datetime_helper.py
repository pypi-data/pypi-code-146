import datetime
from typing import Optional, Union


def create_datetime_str(
    datetime_info: Optional[Union[str, float, datetime.datetime]]
) -> Optional[str]:
    """Creates a RFC 3339 string representation.

    Args:
        datetime_info: If none or a string, returns the input value back. For
            datetime.datetime objects/numbers serialize to a RFC 3339 string.
            Numbers are interpreted as seconds since epoch.
    """
    if not datetime_info or isinstance(datetime_info, str):
        return datetime_info

    if type(datetime_info) == int or type(datetime_info) == float:
        datetime_info = datetime.datetime.fromtimestamp(
            datetime_info, tz=datetime.timezone.utc
        )

    if isinstance(datetime_info, datetime.datetime):
        if not datetime_info.tzinfo:
            # TODO(apoorv) Maybe localize to current timezone instead?
            raise ValueError(
                "Datetime object has no timezone. Please set a timezone explicitly."
            )
        # Per https://stackoverflow.com/a/8556555/354573
        return datetime_info.isoformat("T")

    raise ValueError(
        "Got unexpected argument of type {}: {}".format(
            type(datetime_info), datetime_info
        )
    )
