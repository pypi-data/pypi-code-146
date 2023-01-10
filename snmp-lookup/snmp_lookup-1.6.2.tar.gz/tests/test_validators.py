#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
import pytest
from snmp_lookup.validators import valid_ipaddress
from snmp_lookup.validators import valid_unsigned32
from snmp_lookup.validators import valid_snmp_index
from snmp_lookup.validators import valid_mac


def test_ipv4():
    assert valid_ipaddress("127.0.0.1")
    with pytest.raises(ValueError):
        valid_ipaddress("localhost")


def test_valid_unsigned32():
    assert valid_unsigned32("12")
    assert valid_unsigned32(12)
    assert valid_unsigned32("-12") is False
    assert valid_unsigned32("0")


def test_valid_nonnegative():
    from snmp_lookup.validators import valid_non_negative_integer

    assert valid_non_negative_integer("0") is True
    assert valid_non_negative_integer("1") is True
    assert valid_non_negative_integer("2147483647") is True
    assert valid_non_negative_integer("-1") is False


def test_valid_positive():
    from snmp_lookup.validators import valid_positive_integer

    assert valid_positive_integer("1") is True
    assert valid_positive_integer("2147483647") is True
    assert valid_positive_integer("0") is False
    assert valid_positive_integer("-1") is False


def test_valid_snmp_index():
    assert valid_snmp_index("1.3.6.1.4.1.6574.5.1.1.2.5")
    assert valid_snmp_index("1.3.6.1.2.1.1.2.0")


def test_valid_mac():
    assert valid_mac("00:11:22:33:44:55")
    assert valid_mac("AA:BB:22:33:44:55")
    assert valid_mac("00:11:22:33:44:ff")
    assert not valid_mac("XX:11:22:33:44:55")
    assert not valid_mac("0:0:1:22:33:44:55")
    assert not valid_mac("00:-1:22:33:44:55")
    assert not valid_mac("-3_0e:0:0:0:00:00")
