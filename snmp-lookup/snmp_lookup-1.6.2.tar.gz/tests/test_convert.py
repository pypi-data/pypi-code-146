#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Test convertion roundtrips."""
from decimal import Decimal

import pytest

from snmp_lookup.convert import (
    scale_from_snmp,
    scale_to_snmp,
    decimal_string,
    zabbix_datatype,
)


def test_convert_from_factor_0():
    """Division by zero."""
    with pytest.raises(ValueError):
        scale_from_snmp(12, Decimal(0))
    with pytest.raises(ValueError):
        scale_from_snmp(12, factor=None)
    with pytest.raises(ValueError):
        scale_from_snmp(12, factor="")
    with pytest.raises(ValueError):
        scale_from_snmp(12, factor=0)


def test_decimal_string():
    """Decimal string convertions."""
    with pytest.raises(ArithmeticError):
        decimal_string("1/abcdef")

    with pytest.raises(ArithmeticError):
        decimal_string("2/32")

    with pytest.raises(ArithmeticError):
        decimal_string("1/")

    assert decimal_string("3600") == Decimal("3600")
    assert decimal_string("1/3600E4") == (Decimal(1) / Decimal("3600E4"))


def test_scale_factor_one():
    """No change, we hope we hope."""
    assert scale_from_snmp(12, Decimal(1)) == "12"
    assert scale_from_snmp(0, Decimal(1)) == "0"
    assert scale_from_snmp(132, Decimal(1)) == "132"


def test_scale_factor_big():
    """Scaling down should return precise amount of decimals."""
    assert scale_from_snmp(12, Decimal("1000")) == "12000"
    assert scale_from_snmp(12, Decimal("3600")) == "43200"
    assert scale_from_snmp(12, Decimal("2E5")) == "2400000"


def test_scale_factor_small():
    """Scaling up should work even when we don't expect it to happen."""
    assert scale_from_snmp(120000, Decimal("0.0001")) == "12"
    assert scale_from_snmp(10000, Decimal("0.001")) == "10"
    assert scale_from_snmp(4000, Decimal("0.003")) == "12"
    assert scale_from_snmp(3000000, Decimal("0.000004")) == "12"


FACTORS = [
    "0.0000333333",
    "0.001",
    "0.003",
    "0.1",
    "1",
    "10",
    "1000",
    "100000",
]


@pytest.mark.parametrize("str_factor", FACTORS)
def test_scale_roundtrip(str_factor):
    """Round trips should be exact."""
    factor = Decimal(str_factor)
    converted = scale_from_snmp(13, factor)
    assert 13 == scale_to_snmp(converted, factor)


@pytest.mark.parametrize("str_factor", FACTORS)
def test_scale_roundtrip_large(str_factor):
    """Round trips should be exact."""
    factor = Decimal(str_factor)
    # 240000003001  has an error of 5191  when using float
    converted = scale_from_snmp(240000003001, factor)
    assert 240000003001 == scale_to_snmp(converted, factor)


def test_datatype_things():
    LARGE_INT = 1 << 32
    SMALLER_INT = 1 << 30
    assert zabbix_datatype("Counter32", Decimal(LARGE_INT)) == "float"
    assert zabbix_datatype("Counter32", Decimal(SMALLER_INT)) == "uint64"
    assert zabbix_datatype("Counter32", Decimal(-1)) == "float"
    assert zabbix_datatype("Integer32", Decimal(-1)) == "float"
    assert zabbix_datatype("Integer32", Decimal(1)) == "float"
    assert zabbix_datatype("Integer32", Decimal(1.1)) == "float"
    assert zabbix_datatype("Counter64", Decimal(2)) == "float"
    assert zabbix_datatype("Counter64", Decimal(1.2)) == "float"
    assert zabbix_datatype("Counter64", Decimal(1)) == "uint64"
