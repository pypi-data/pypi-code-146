#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
import pytest

from snmp_lookup.helpers import break_key, oid_split


def test_break_invalid_key():
    KEY = "modio.snmp.foo.bar.baz"
    with pytest.raises(ValueError):
        break_key(KEY)

    KEY = "snmp.Foo.bar"
    with pytest.raises(ValueError):
        break_key(KEY)


def test_break_key():
    KEY = "snmp.spindel.unifiSW.foo.bar"
    kind, name, part = break_key(KEY)
    assert part == "foo.bar"
    assert kind == "unifiSW"
    assert name == "spindel"


def test_oid_split():
    OID = "1.2.3.4.5.6.2"
    val = oid_split(OID)
    assert val[0] == 1

    OID = "foobar.1"
    val = oid_split(OID)
    assert val[0] == "foobar"
    assert val[1] == 1
