# SPDX-License-Identifier: AGPL-3.0-or-later
"""Data conversion utilities."""

from decimal import Decimal
from typing import Set

_ONE = Decimal(1)

__all__ = [
    "decimal_string",
    "decimal_is_integer",
    "scale_from_snmp",
    "scale_to_snmp",
    "zabbix_datatype",
]


def decimal_string(indata: str) -> Decimal:
    """Parse a string, raising error if it's not as expected."""
    if indata.startswith("1/"):
        val = indata[2:]
        res = _ONE / Decimal(val)
        return res

    res = Decimal(indata)
    return res


def decimal_is_integer(val: Decimal) -> bool:
    """Test if a decimal is an Integer or not."""
    return val == val.to_integral()


def scale_from_snmp(object_value: int, factor: Decimal) -> str:
    """Scale transform a value.

    ex:  0.1 mOhm  => Ohm
    """
    if not factor:
        raise ValueError("Cast only when point has a factor.")

    number = Decimal(object_value)

    conv = number * factor

    # If it's equal to an integer, restore precision to integer by Quantizing
    # to 0 decimals
    if conv == conv.to_integral_value():
        conv = conv.quantize(_ONE)
    else:
        # Not an integer. Normalize the number
        conv = conv.normalize()
    return str(conv)


def scale_to_snmp(input_value: str, factor: Decimal) -> int:
    """Scale from something to integer for snmp representation."""
    number = Decimal(input_value)
    conv = number / factor

    # if scaling happened towards a larger number,
    # adjust amount of decimals of the output
    if -1 < factor < 1:
        conv = conv.quantize(_ONE)

    val = conv.to_integral_value()
    return int(val)


# One larger than 32bit maxint. Multiply a 32bit maxint with this, and we break
# uint64 maths.
MAX_INT_FACTOR = 1 << 32
FLOAT = "float"
UINT = "uint64"

# Set of types.
DATATYPE_64 = {"Counter64"}
DATATYPE_ALL_NEGATIVE: Set[str] = set()
DATATYPE_SIGNED_INTEGER = {
    "Integer32",
    "Integer",
}


def zabbix_datatype(snmp_datatype: str, factor: Decimal) -> str:
    # pylint: disable=R0911
    """Look at SNMP datatype and factor, deduce zabbix datatype."""
    # match : float / integer
    if not decimal_is_integer(factor):
        return FLOAT

    # Is integer.  Negative?
    if factor < 0:
        if snmp_datatype in DATATYPE_ALL_NEGATIVE:
            return UINT
        return FLOAT

    #
    # factor is now non-negative integer only
    #

    # Zabbix has no support for signed integers.
    if snmp_datatype in DATATYPE_SIGNED_INTEGER:
        return FLOAT

    if factor > 1 and snmp_datatype in DATATYPE_64:
        # 64bit int scaled by an int can become > int
        return FLOAT

    # Factor is too large to safely represent
    if factor >= MAX_INT_FACTOR:
        return FLOAT

    return UINT
