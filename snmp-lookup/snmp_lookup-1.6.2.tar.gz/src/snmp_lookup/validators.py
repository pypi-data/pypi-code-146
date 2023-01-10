# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Validator functions.

Misc functions to do with data validation.
"""

import re
from string import ascii_letters, digits, hexdigits
from typing import Callable

from .helpers import break_key
from .helpers import oid_split
from .kind import KINDS, get_kind

NAME_VALID_RE = r"^[a-zA-Z0-9_]{2,14}\Z"
OK_KEYPART_CHARS = set(ascii_letters + digits + "._-")
OK_HEX = set(hexdigits)


__all__ = [
    "valid_name",
    "valid_key",
    "valid_kind",
    "break_key",
    "VALIDATORS",
    "valid_mac",
]


def get_validator(typ: str) -> Callable:
    """Get a validator for the SNMP datatype type."""
    assert typ in VALIDATORS
    return VALIDATORS[typ]


def valid_unsigned32(indata: str) -> bool:
    """Test that indata is a valid 32bit unsigned."""
    val = int(indata)
    return 0 <= val <= 4294967295


def valid_non_negative_integer(indata: str) -> bool:
    """Not a negative number."""
    val = int(indata)
    return 0 <= val <= 2147483647


def valid_positive_integer(indata: str) -> bool:
    """Not a negative number, and one more."""
    val = int(indata)
    return 1 <= val <= 2147483647


def valid_ipaddress(indata: str) -> bool:
    """Test if indata is a valid ip-address."""
    # pylint: disable=import-outside-toplevel
    import ipaddress

    val = ipaddress.IPv4Address(indata)
    return bool(val)


def valid_string(indata: str) -> bool:
    """Test that indata is a string."""
    return isinstance(indata, str)


def valid_name(name: str) -> bool:
    """Test a name if it is valid."""
    result = re.match(NAME_VALID_RE, name)
    return bool(result)


def valid_signed32(indata: str) -> bool:
    """Test if an indata is valid signed 32 bit."""
    val = int(indata)
    return -2147483648 <= val <= 2147483647


def valid_unsigned64(indata: str) -> bool:
    """Test for validity of unsigned 64-bit."""
    val = int(indata)
    return 0 <= val <= 2**63


def valid_kind(kind: str) -> bool:
    """Test if a kind is valid."""
    if valid_name(kind):
        return kind in KINDS
    return False


def valid_keypart(keypart: str) -> bool:
    """Test if a part of a key (latter part) is valid."""
    if keypart.startswith("."):
        return False

    if keypart.endswith("."):
        return False

    if set(keypart) > OK_KEYPART_CHARS:
        return False

    return True


def valid_key(key: str) -> bool:
    """Test if a key is valid."""
    kind, name, part = break_key(key)
    if not valid_name(name):
        return False

    if not valid_kind(kind):
        return False

    if not valid_keypart(part):
        return False

    resolved = get_kind(kind)
    if part not in resolved.point_by_key:
        return False

    return True


OK_NUMERIC_OID_CHAR = set("1234567890.")


def valid_numeric_oid(oid: str) -> bool:
    """Test that an oid is valid according to numerical rules.

    Ex: "1.3.6.1.4.1.4413.1.1.1.2.15.10.1.8.0"
    """
    # Invalid characters for a numeric oid
    if set(oid) > OK_NUMERIC_OID_CHAR:
        return False

    # Turn it into a split tuple
    split = oid_split(oid)
    # split == (1, 2,5 ,69, 127, 0, 0, 1)

    # Re-combine with periods in between
    rejoin = ".".join(str(i) for i in split)

    # rejoin = "1.2.5.69.127.0.0.1"
    return rejoin == oid


def valid_snmp_index(snmp_index: str) -> bool:
    """Quickly check if an snmp-index is valid."""
    if not snmp_index:
        # empty snmp_index is not valid, should be "0" on a non-tabled item
        return False

    if snmp_index.strip() != snmp_index:
        # Whitespace must not be part
        return False

    # Single digit? Thats ok
    if snmp_index.isnumeric():
        return True

    # Its not purely numeric? Should contain periods.
    if "." not in snmp_index:
        return False

    parts = snmp_index.split(".")
    if all(x.isnumeric() for x in parts):
        return True
    return False


def valid_mac(value: str) -> bool:
    """Try to deduce that it's a mac address.

    00:00:00:00:00:00
    """
    if len(value) != 17:
        return False

    parts = value.split(":")
    if len(parts) != 6:
        return False

    lengths = (len(x) == 2 for x in parts)
    if not all(lengths):
        return False

    hexed = (OK_HEX.issuperset(x) for x in parts)
    if not all(hexed):
        return False

    return True


VALIDATORS = {
    "Counter32": valid_unsigned32,
    "Gauge32": valid_unsigned32,
    "Unsigned32": valid_unsigned32,
    "Integer32": valid_signed32,
    "IpAddress": valid_ipaddress,
    "DisplayString": valid_string,
    "OctetString": valid_string,
    "Counter64": valid_unsigned64,
    "PhysAddress": valid_mac,
    "NonNegativeInteger": valid_non_negative_integer,
    "PositiveInteger": valid_positive_integer,
}
