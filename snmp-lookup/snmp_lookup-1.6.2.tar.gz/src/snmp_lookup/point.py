# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Point handling to assist on-device code.

Deals with pysnmp internals to get a bit less memory churn and consumption.
"""

from typing import Dict, Sequence

from pysnmp.smi.rfc1902 import ObjectIdentity  # type: ignore
from pysnmp.smi.builder import ZipMibSource  # type: ignore
from pysnmp.smi.view import MibViewController  # type: ignore
from pysnmp.hlapi.varbinds import AbstractVarBinds  # type: ignore
from pysnmp.entity.engine import SnmpEngine  # type: ignore


from .kind import Point

OICache = Dict[str, ObjectIdentity]

SCAN_STARTPOINTS = [
    ObjectIdentity("SNMPv2-MIB", "sysDescr"),
    ObjectIdentity("SNMPv2-SMI", "enterprises"),
]


def get_view_controller(engine: SnmpEngine) -> MibViewController:
    """I hate the pysnmp interfaces."""
    # Because an engine has a .getMibBuilder  but not a .getMibViewController,
    # instead "getMibViewController" is implemented as a staticmethod on an
    # abstract class mixin.
    return AbstractVarBinds.getMibViewController(engine)


def add_mibs(engine: SnmpEngine) -> None:
    """Add the built-in mibs to this engines instance.

    Try to only call it once.
    """
    builder = engine.getMibBuilder()
    # This declares a source of MIB files from inside the snmp_lookup package.
    my_source = ZipMibSource("snmp_lookup.mibs")
    # This adds the mib source to the builder that belongs to the view.
    builder.addMibSources(my_source)

    # Since we have loaded the MIBs, take the time to resolve our
    # SCAN_STARTPOINTS
    view = get_view_controller(engine)
    for oid in SCAN_STARTPOINTS:
        oid.resolveWithMib(view)


def resolve_with_mibs(
    points: Sequence[Point], cache: OICache, engine: SnmpEngine
) -> None:
    """Resolve all points with the Engine.

    This ensures that all pysnmp rfc1902.ObjectIdentity() are singletons as
    needed.
    """
    view = get_view_controller(engine)
    for point in points:
        if point.oi is not None:
            continue
        if point.oid not in cache:
            _oi = ObjectIdentity(point.oid)
            # Mark this oid to load the MIB required from the datasource above.
            _oi.loadMibs(point.mib)
            # Actually resolve the mib
            _oi.resolveWithMib(view)
            cache[point.oid] = _oi
        point.oi = cache[point.oid]
