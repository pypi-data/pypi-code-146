# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Kind and Device handling.

Parse a CSV file and return application-suitable data.

Nothing in this code should EVER need to use `pysnmp` as it is, as it should
always return data that's suitable to be used without pysnmp or other dependent
libraries.

"""


import csv
from typing import Dict, Generator, Sequence, List, TextIO

import importlib_resources as resources

from .helpers import break_key
from .data import SNMP_CSV_ITEMS
from .data import all_datafiles
from .convert import (
    decimal_string,
    zabbix_datatype,
)

assert SNMP_CSV_ITEMS

# __all__ = ["KINDS", "get_kind"]

KEY_FORMAT = "snmp.{device}.{kind}.{keypart}"


class Point:
    # pylint: disable=too-many-instance-attributes
    """Metadata for an SNMP OID datapoint.

    Extra data: name, description, mib, key and which kind
    """

    def __init__(
        self,
        *,
        snmp_mib: str,
        snmp_label: str,
        snmp_index: str,
        snmp_oid: str,
        snmp_datatype: str,
        name: str,
        description: str,
        keypart: str,
        kind: str,
        units: str,
        units_factor: str,
    ):
        """Initialize a Point. Maps 1:1 with a line in a CSV file."""
        self.mib = snmp_mib
        self.label = snmp_label
        self.index = snmp_index
        self.oid = snmp_oid
        self.datatype = snmp_datatype
        self.name = name
        self.description = description
        self.keypart = keypart
        self.kind = kind
        self.units = units
        self.oi = None  # pylint: disable=invalid-name
        self.units_factor = None
        self.zabbix_unit = None
        if units_factor:
            self.units_factor = decimal_string(units_factor)
            self.zabbix_unit = zabbix_datatype(
                self.datatype, self.units_factor
            )

    def __repr__(self) -> str:
        """Print in format useful for net-snmp."""
        return f"{self.mib}::{self.label}.{self.index} - {self.name}"

    def to_key(self, device: str) -> str:
        """Generate a modio submit-style key for this datapoint."""
        return KEY_FORMAT.format(
            device=device, kind=self.kind, keypart=self.keypart
        )


class Kind:
    """Kind, for lack of a better name, is a type of device that we monitor."""

    def __init__(self, kind: str, description: str):
        """Shallow object matching a kind.

        For lack of better words, "kind" is a gathering of data-points matching
        a sort of device, with some metadata.
        """
        self.kind = kind
        self.description = description
        self._points: List[Point] = []
        self._bykey: Dict[str, Point] = {}

    @property
    def points(self) -> Sequence[Point]:
        """Return all points associated with this Kind."""
        if not self._points:
            self._points = load_points(kind=self.kind)
        return self._points

    @property
    def point_by_key(self) -> Dict[str, Point]:
        """Return a mapping of keypart: Point."""
        if not self._bykey:
            self._bykey = {x.keypart: x for x in self.points}
        return self._bykey


def get_points(kind: str) -> Sequence[Point]:
    """Return all points for that kind."""
    the_kind = get_kind(kind)
    return the_kind.points


def get_point(key: str = "snmp.foo.bar.baz") -> Point:
    """Return a Point matching key."""
    kind_name, _, part = break_key(key)
    kind = get_kind(kind_name)
    point = kind.point_by_key[part]
    return point


def get_snmp_type(key: str = "snmp.foo.bar.baz") -> str:
    """Return an SNMP type for a datapoint."""
    point = get_point(key)
    datatype = point.datatype
    return datatype


def get_kinds() -> Generator[str, None, None]:
    """Iterate over all valid names of kinds."""
    for fname in all_datafiles():
        if fname.endswith(".csv"):
            yield fname.rsplit(".", maxsplit=1)[0]


_KINDS: Dict[str, Kind] = {}


def get_kind(kind: str) -> Kind:
    """Return an instantiated kind."""
    assert kind in KINDS

    # Lazy cache of kinds
    if kind not in _KINDS:
        my_kind = Kind(kind=kind, description="sniff first line of csv?")
        _KINDS[kind] = my_kind
    return _KINDS[kind]


def get_alerts(kind: str) -> None:
    """Get alerts for a kind."""
    raise NotImplementedError("No alerts for snmp yet")


def get_mibs(kind: str) -> Sequence[str]:
    """Return all mibs this kind requires."""
    the_kind = get_kind(kind)
    result = [point.mib for point in the_kind.points]
    return result


def load_points(kind: str) -> List[Point]:
    """Load datapoints for this kind."""
    mod_path = resources.files("snmp_lookup.data") / f"{kind}.csv"
    with resources.as_file(mod_path) as path:
        with path.open(encoding="utf8") as fil:
            return _points_from_csv(fil, kind=kind)


def _points_from_csv(fobj: TextIO, kind: str) -> List[Point]:
    """Parse an opened csv file into Point objects."""
    result = []
    reader = csv.DictReader(fobj, delimiter=";")
    for line in reader:
        obj = Point(kind=kind, **line)
        result.append(obj)
    return result


KINDS = list(get_kinds())
