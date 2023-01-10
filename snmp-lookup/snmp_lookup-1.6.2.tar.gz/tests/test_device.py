#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
from snmp_lookup import get_kind, get_point
from snmp_lookup.point import resolve_with_mibs, add_mibs
from pysnmp.hlapi.varbinds import AbstractVarBinds
from pysnmp.hlapi import SnmpEngine


def test_device_basics():
    engine = SnmpEngine()
    add_mibs(engine)

    the_kind = get_kind("printer")
    cache = {}

    for point in the_kind.points:
        assert point.oi is None

    resolve_with_mibs(the_kind.points, cache, engine)

    for point in the_kind.points:
        assert point.oi is not None


def test_device_singleton_objectidentity():
    """Ensure that the resolved oids are singletons."""
    engine = SnmpEngine()
    add_mibs(engine)

    ap01 = get_kind("unifiAP")
    ap02 = get_kind("unifiAP")
    cache = {}

    first = ap01.points[0]
    second = ap02.points[0]

    assert first.oid == second.oid

    resolve_with_mibs(ap01.points, cache, engine)
    assert first.oi is not None

    resolve_with_mibs(ap02.points, cache, engine)
    assert second.oi is not None
    assert first.oi is second.oi


def test_device_units_scaling_large_integer():
    """Test against a known key that scales Wh to Joules."""
    point = get_point("snmp.NAME.enoc_pdu.L1.energy")
    assert point.units == "J"
    assert point.units_factor > 3600
    assert point.datatype == "Integer32"
    # Signed integer * integer factor == float
    assert point.zabbix_unit == "float"


def test_device_units_scaling_small_float():
    """Test against a known key that scales deciAmpere to Ampere."""
    point = get_point("snmp.NAME.enoc_pdu.L1.current")
    assert point.units == "A"
    assert point.units_factor < 1
    # Signed Integer * float factor == float
    assert point.datatype == "Integer32"
    assert point.zabbix_unit == "float"


def test_device_units_scaling_common_uint():
    """Test against a known key that HectoWatt to Watt."""
    point = get_point("snmp.NAME.socomec.input.1.true_power")

    assert point.units_factor == 100
    assert point.units == "W"
    assert point.datatype == "NonNegativeInteger"
    # Positive 32bit integer times small integer factor == 64bit unsigned
    assert point.zabbix_unit == "uint64"


def test_device_units_scaling_fixpoint_float():
    """Test against a known key that has Volt as a centiVolt"""
    point = get_point("snmp.NAME.bacs2.mod.0.voltage")
    assert 0 < point.units_factor < 1
    assert point.units == "V"
    assert point.datatype == "PositiveInteger"
    # Positive 32bit integer times small floating point factor == float
    assert point.zabbix_unit == "float"
