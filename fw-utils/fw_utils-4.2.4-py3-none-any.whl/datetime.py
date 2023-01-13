"""Datetime helpers."""
import re
import typing as t
from datetime import datetime, tzinfo

import dateutil.parser as dt_parser
import tzlocal

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    from backports.zoneinfo import ZoneInfo  # type: ignore

__all__ = [
    "ZoneInfo",  # brazenly expose for proxied imports
    "format_datetime",
    "get_datetime",
    "get_tzinfo",
]


def format_datetime(dt: datetime):
    """Return ISO-formatted datetime with millisecond precision."""
    return dt.isoformat(timespec="milliseconds")


def get_datetime(
    value: t.Union[str, int, float, datetime] = "now",
    *,
    sub: t.Union[t.Tuple[str, str], t.List[t.Tuple[str, str]]] = None,
    fmt: t.Union[str, t.List[str]] = None,
    tz: t.Union[str, tzinfo] = None,
) -> datetime:
    """Return datetime object parsed from a string/number (or now w/o value)."""
    tz = get_tzinfo(tz)
    assert isinstance(tz, tzinfo)
    if value == "now":
        return datetime.now(tz=tz)
    if not isinstance(value, (str, int, float, datetime)):
        msg = f"Expected int, str or datetime (got {value.__class__.__name__!r})"
        raise TypeError(msg)

    def set_tz(dt_obj: datetime):
        assert isinstance(tz, tzinfo)
        if dt_obj.tzinfo is None:
            dt_obj = dt_obj.replace(tzinfo=tz)
        dt_obj = dt_obj.astimezone(tz)
        return dt_obj

    if isinstance(value, (int, float)):
        return set_tz(datetime.fromtimestamp(value, tz=tz))
    if isinstance(value, datetime):
        return set_tz(value)
    # apply substitutions if specified
    sub = sub or []
    if len(sub) == 2 and isinstance(sub[0], str):
        sub = [t.cast(t.Tuple[str, str], sub)]
    for pattern, repl in t.cast(t.List[t.Tuple[str, str]], sub):
        value = re.sub(pattern, repl, value)
    # parse with dateutil parser when no format is specified
    if not fmt:
        default = datetime(1970, 1, 1, 0, 0, 0)
        try:
            return set_tz(dt_parser.parse(value, default=default))
        except dt_parser.ParserError:
            raise ValueError(f"Can't parse {value!r} with dateutil") from None
    # parse with strptime when formats are specified, use the first match
    fmt = [fmt] if isinstance(fmt, str) else (fmt or [])
    for f in fmt:
        try:
            return set_tz(datetime.strptime(value, f))
        except ValueError:
            pass
    raise ValueError(f"Can't parse {value!r} with strptime: {fmt!r}")


def get_tzinfo(tz: t.Union[str, tzinfo] = None) -> tzinfo:
    """Return tzinfo object for the given tz name (or local zone w/o value)."""
    if not tz:
        tz = tzlocal.get_localzone()
    elif isinstance(tz, str):
        tz = ZoneInfo(tz)
    # tzlocal wraps in a shim - unwrap to expose key
    if hasattr(tz, "unwrap_shim"):
        tz = tz.unwrap_shim()  # type: ignore
    assert isinstance(tz, tzinfo)
    return tz
