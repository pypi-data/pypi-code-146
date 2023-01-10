# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Selftest routines.

Ensure that all our internal oids are consistent and has our desired data.
"""

from typing import Set, Tuple
from .kind import get_kinds
from .kind import get_kind
from .kind import get_mibs
from .kind import get_snmp_type

from .validators import get_validator
from .validators import valid_key
from .validators import VALIDATORS
from .validators import valid_numeric_oid

DEVICE_NAME = "foobar"


def test_keys_look_ok() -> None:
    """Iterates over all kinds/points and checks that all keys are unique."""
    seen: Set[str] = set()
    for kind in get_kinds():
        device = get_kind(kind)
        for point in device.points:
            key = point.to_key(device=DEVICE_NAME)
            if not valid_key(key):
                raise ValueError("Invalid key", key)
            if key in seen:
                raise ValueError("Duplicate key", key)
            seen.add(key)


def test_labels_look_ok() -> None:
    """Iterates over all kinds/points and checks for uniqueness."""
    seen: Set[Tuple[str, str, str, str]] = set()
    for kind in get_kinds():
        device = get_kind(kind)
        for point in device.points:
            tup = (kind, point.mib, point.label, point.index)
            if tup in seen:
                raise ValueError(
                    "Duplicate kind/mib/label/index combination", tup
                )
            seen.add(tup)


def test_oids_look_ok() -> None:
    """Iterates over all kinds/points and checks for uniqueness."""
    seen: Set[Tuple[str, str]] = set()
    for kind in get_kinds():
        device = get_kind(kind)
        for point in device.points:
            tup = (kind, point.oid)
            if not valid_numeric_oid(point.oid):
                raise ValueError("This OID seems invalid", point.oid)
            if tup in seen:
                raise ValueError("Duplicate kind/oid combination", tup)
            seen.add(tup)


def test_mibs_look_ok() -> None:
    """Iterates over all kinds and checks that our mibs seem ok."""
    seen: Set[str] = set()
    for kind in get_kinds():
        if kind in seen:
            raise ValueError("This kind appears twice?", kind)
        seen.add(kind)
        for mib in get_mibs(kind):
            if not isinstance(mib, str):
                raise ValueError("Mibs should be stringly", mib)
            if not mib:
                raise ValueError("Strange mib. Empty?", mib)


def test_points_look_ok() -> None:
    """Ensure all kinds/points has descriptions and names."""
    for kind in get_kinds():
        device = get_kind(kind)
        for point in device.points:
            if not point.name:
                raise ValueError("All datapoints should have a name", point)
            if not point.description:
                raise ValueError(
                    "All datapoints should have a description", point
                )
            if not point.mib:
                raise ValueError("All datapoints should have a mib", point)
            if not point.oid:
                raise ValueError("All datapoints should have an oid", point)


def test_types_look_ok() -> None:
    """Iterates over all kinds/points and ensures we have a basic type info."""
    for kind in get_kinds():
        device = get_kind(kind)
        for point in device.points:
            key = point.to_key(device=DEVICE_NAME)
            typ = get_snmp_type(key)
            if typ not in VALIDATORS:
                raise ValueError("Unknown type? Add to validators", typ)


def test_validators_look_ok() -> None:
    """Iterates over all kinds/points and ensures we have a basic validator."""
    for kind in get_kinds():
        device = get_kind(kind)
        for point in device.points:
            key = point.to_key(device=DEVICE_NAME)
            typ = get_snmp_type(key)
            validator = get_validator(typ)
            if not callable(validator):
                raise ValueError("Missing validator for key", key)


def test_import_looks_ok() -> None:
    """Validation test that our code doesn't need pysnmp loaded."""
    try:
        # pylint: disable=C0415
        import pysnmp  # type: ignore

        print(pysnmp)

        assert pysnmp
        raise RuntimeError("pysnmp is available")
    except ImportError:
        pass


def run_selftest() -> None:
    """Run self validation tests."""
    test_mibs_look_ok()
    test_points_look_ok()
    test_labels_look_ok()
    test_oids_look_ok()
    test_keys_look_ok()
    test_types_look_ok()
    test_validators_look_ok()
