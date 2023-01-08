"""Default metadata for selected standard library types."""


import datetime
import ipaddress
import pathlib
import re
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Mapping, Pattern, TypeVar

import dateutil.parser
from typing_extensions import Final

from .classes import VALUE, auto
from .errors import ValidationException
from .metadata import TargetMetadata, with_
from .types import Target


@dataclass(frozen=True)
class StdlibValidationException(ValidationException):
    """Exception type raised on failure by standard library constructors."""

    msg: str


@auto(from_=VALUE)
def _make_datetime(s: str) -> datetime.datetime:
    try:
        return dateutil.parser.isoparse(s)
    except ValueError as e:
        raise StdlibValidationException("invalid ISO-8601 datetime") from e


@auto(from_=VALUE)
def _make_regex(s: str) -> Pattern[Any]:
    try:
        return re.compile(s)
    except re.error as e:
        raise StdlibValidationException(f"invalid regex: {e}") from e


@auto(from_=VALUE)
def _make_ipv4_address(s: str) -> ipaddress.IPv4Address:
    try:
        return ipaddress.IPv4Address(s)
    except ValueError as e:
        raise StdlibValidationException(f"invalid IPv4 address: {e}") from e


@auto(from_=VALUE)
def _make_ipv6_address(s: str) -> ipaddress.IPv6Address:
    try:
        return ipaddress.IPv6Address(s)
    except ValueError as e:
        raise StdlibValidationException(f"invalid IPv6 address: {e}") from e


T = TypeVar("T")


def _make_str_fn(path_t: Callable[[str], T]) -> Callable[[str], T]:
    @auto(from_=VALUE)
    def _make_path(s: str) -> T:
        return path_t(s)

    return _make_path


DEFAULT_METADATA: Final[Mapping[Target[Any], TargetMetadata]] = {
    datetime.datetime: [with_(lambda: _make_datetime)],
    Pattern: [with_(lambda: _make_regex)],
    Pattern[str]: [with_(lambda: _make_regex)],
    ipaddress.IPv4Address: [with_(lambda: _make_ipv4_address)],
    ipaddress.IPv6Address: [with_(lambda: _make_ipv6_address)],
    **{
        t: [with_(partial(_make_str_fn, t))]
        for t in [
            pathlib.Path,
            pathlib.PosixPath,
            pathlib.WindowsPath,
            pathlib.PurePath,
            pathlib.PurePosixPath,
            pathlib.PureWindowsPath,
        ]
    },
}
