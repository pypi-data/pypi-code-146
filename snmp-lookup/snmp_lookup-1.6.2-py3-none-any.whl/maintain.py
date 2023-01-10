# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Maintain: A module which works on our CSV files.

This module handles csv file to MIB parsing and re-writing, making sure that
CSV files are complete, correct (or fixes them) and works together with the
pysnmp and the smi libraries to resolve them into useful data-formats.
"""

import argparse
import csv
import os
import pathlib
import tempfile
import logging

from typing import Any, Dict, IO, Iterable, List, Optional
from typing import Set, Tuple, TextIO, Callable

from pysnmp.hlapi import ObjectIdentity, ObjectType  # type: ignore
from pysnmp.smi.builder import MibBuilder, ZipMibSource  # type: ignore
from pysnmp.smi.view import MibViewController  # type: ignore
from pysnmp.smi.error import MibLoadError, SmiError  # type: ignore

try:
    # Python 3.8+ feature
    from importlib import resources as importlib_resources
except (AttributeError, ImportError):
    import importlib_resources  # type: ignore

from .convert import decimal_string

from .validators import valid_numeric_oid
from .validators import valid_snmp_index
from .validators import VALIDATORS
from .validators import valid_keypart

from .helpers import oid_split
from .helpers import reseek_file
from .data import SNMP_CSV_ITEMS
from .data import check_csv_header
from .data import all_datafiles
from .senml import SENML_UNITS

Line = Dict[str, str]

LOG = logging.getLogger(__name__)
FIXER = LOG.getChild("fix")
CHECK = LOG.getChild("check")
RESOLVE = LOG.getChild("resolve")
INDEX = RESOLVE.getChild("index")

# Reserved for internal use. They are valid keyparts, but not valid in data
# files.
RESERVED_KEYPARTS = [
    "read.success",
    "read.error",
    "write.success",
    "write.error",
]

# Maintain doesn't have a public api for others, it's all internal for mib
# managment
__all__ = ["main"]


# This should be the only place where the headers for our CSV files is
# hard-coded, and is only used for validation
# All other code sniffs the headers and uses them as-is.


_mibBuilder = None  # pylint:disable=invalid-name
_mibView = None  # pylint:disable=invalid-name


def get_builder() -> Tuple[MibBuilder, MibViewController]:
    """Return the global builder/Viewer objects once instantiated."""
    # pylint:disable=global-statement,invalid-name
    global _mibBuilder
    global _mibView

    if _mibBuilder is None:
        _mibBuilder = MibBuilder()
        _mibBuilder.loadTexts = True
        _mibBuilder.addMibSources(ZipMibSource("snmp_lookup.mibs"))
        # Warning, this one causes a large amount of memory.
        _mibBuilder.loadModules()
    if _mibView is None:
        _mibView = MibViewController(_mibBuilder)
    return _mibBuilder, _mibView


def try_to_find_mib(text_oid: str) -> str:
    """Attempt to find a MIB which text_oid is declared.

    Not really supposed to be used, but can be useful to resolve unknowns.
    """
    _, mib_view = get_builder()

    entity = oid_split(text_oid)
    # Try to resolve it as a name (label)
    obj = ObjectIdentity(entity)
    obj.resolveWithMib(mib_view)

    mib_name, _, _ = obj.getMibSymbol()
    return mib_name


def resolving_mib(text_mib: str) -> bool:
    """Test if a mib is resolvable."""
    mib_builder, _ = get_builder()
    try:
        mib_builder.loadModule(text_mib)
    except MibLoadError:
        return False
    return True


def resolve_oid(text_mib: str, text_oid: str) -> ObjectIdentity:
    """Resolve a text oid and mib to canonical human format."""
    mib_builder, mib_view = get_builder()
    if text_mib:
        mib_builder.loadModule(text_mib)

    entity = oid_split(text_oid)

    try:
        # If the mib was in numeric format, try to resolve direct to an
        # Identity without going through the "mibView" to get an OID first
        obj = ObjectIdentity(entity, modName=text_mib)
        obj.resolveWithMib(mib_view)
        return obj
    except Exception as exc:  # pylint:disable=broad-except
        LOG.error("Error resolving %s,  Exception: %s", entity, exc)

    print("Difficult resolution, going via mibViewer")
    # See if we can resolve it as a node name in the labelled tree
    oid, label, suffix = mib_view.getNodeName(entity, modName=text_mib)
    print("label == ", label)
    print("suffix ==", suffix)
    # If the mib is in the "NAME" format, try to resolve like that
    obj = ObjectIdentity(oid, modName=text_mib)
    obj.resolveWithMib(mib_view)
    return obj


def get_datatype_name(text_mib: str, text_oid: str) -> str:
    """Return datatype for MIB+Label (or oid)."""
    obj = resolve_oid(text_mib, text_oid)
    node = obj.getMibNode()

    typename = node.__class__.__name__
    if typename == "MibTable":
        raise ValueError("Tables do not have a type", node)

    if not hasattr(node, "syntax"):
        raise ValueError("No syntax for this node?", node)

    datatype = node.syntax.__class__.__name__
    return datatype


def get_datatype(text_mib: str, text_oid: str) -> ObjectType:
    """Return datatype for MIB+Label (or oid)."""
    obj = resolve_oid(text_mib, text_oid)
    node = obj.getMibNode()

    typename = node.__class__.__name__
    if typename == "MibTable":
        raise ValueError("Tables do not have a type", node)

    if not hasattr(node, "syntax"):
        raise ValueError("No syntax for this node?", node)

    return node.syntax


def get_description(text_mib: str, text_oid: str) -> str:
    """Return description for MIB+Label (or oid)."""
    obj = resolve_oid(text_mib, text_oid)
    node = obj.getMibNode()
    description = node.getDescription()
    description = description.strip()
    return description


def get_units(text_mib: str, text_oid: str) -> str:
    """Return units for MIB+Label (or oid)."""
    obj = resolve_oid(text_mib, text_oid)
    node = obj.getMibNode()
    units = node.getUnits()
    units = units.strip()
    return units


def get_numeric_oid(text_mib: str, text_oid: str) -> str:
    """Take a MIB and a Text Label (or text OID) and returns an OID."""
    obj = resolve_oid(text_mib, text_oid)
    return str(obj)


def resolve_names(
    text_mib: str, text_oid: str
) -> Tuple[str, str, Optional[str]]:
    """Look up mib and oid, and returns normalized names."""
    obj = resolve_oid(text_mib, text_oid)
    res_mib, res_oid, index = obj.getMibSymbol()

    index_part = None
    RESOLVE.debug("Resolved MIB '%s' to '%s'", text_mib, res_mib)
    RESOLVE.debug("Resolved OID '%s' to '%s'", text_oid, res_oid)

    def bang(val: Any) -> str:
        """Take an asn1 index type and convert to string.

        Indata is an instance of a ObjectIndex or other asn1 index
        type and transform it to a resolve-able string part.

        We cannot just use pretty-print as then a hex-encoded thing (or enum)
        would be formatted "wrongly" for our usecase.

        This hasn't really been tried well with "abstract" null-like index
        values as those in routing tables.
        """
        INDEX.debug("Index resolving on:\n %s", val)
        # If it's an int, treat it easily.
        #  pylint: disable=protected-access
        if isinstance(val._value, int):
            return str(val._value)

        # Check if we can get a value for it, and if so, print it as -is.
        try:
            new_val = val.getValue()
            pretty = new_val.prettyPrint()
            INDEX.debug("Pretty Val: %s", pretty)
        except AttributeError:
            pretty = val.prettyPrint()
            INDEX.debug("Pure val: %s", pretty)
        return pretty

    if index:
        INDEX.debug("OID has an index.. this is complex: %s", index)
        index_part = ".".join(bang(v) for v in index)
    RESOLVE.debug("OID %s has index part: %s", text_oid, index_part)

    # Some more debug-code below.
    is_debugging = False
    if index and is_debugging:
        with_values = [v for v in index if v.hasValue()]
        # Print all the index values. Some debugging needed
        for val in with_values:
            print(f"Index: {val.prettyPrintType()}  => {val.prettyPrint()}")
    return res_mib, res_oid, index_part


def resolve_mib_label_index(mib: str, label: str, index: str) -> str:
    """Take MIB, Label and Index and return an numerical OID."""
    oid = get_numeric_oid(mib, label)
    if index:
        split_index = oid_split(index)
        split_oid = oid_split(oid)
        new_oid = split_oid + split_index
        oid = ".".join(str(x) for x in new_oid)
    return oid


def fix_single_line(line: Line) -> Dict[str, Optional[str]]:
    """Attempt to fix a single line in a CSV file."""

    def neat(_value: Optional[str]) -> Optional[str]:
        if _value:
            return _value.strip()
        return _value

    # pre-fill the "new" data with all data from our line.
    new = {key: neat(val) for key, val in line.items()}
    #    FIXER.debug("Fixing line %s", line)

    old_index = line["snmp_index"]
    old_mib = line["snmp_mib"]
    old_label = line["snmp_label"]
    old_oid = line.get("snmp_oid")

    if not old_oid:
        FIXER.debug(
            "No OID, resolving %s::%s.%s", old_mib, old_label, old_index
        )
        old_oid = resolve_mib_label_index(old_mib, old_label, old_index)
        FIXER.info(
            "Missing numeric oid. Resolved %s::%s.%s => %s",
            old_mib,
            old_label,
            old_index,
            old_oid,
        )

    oid = get_numeric_oid("", old_oid)

    mib, label, index = resolve_names(old_mib, oid)
    # index=None is a Special case.
    # we always want the index.0 to be compatible with net-snmp

    # $ snmpget -v2c -c public  192.168.10.21 SNMPv2-MIB::sysContact.0
    # SNMPv2-MIB::sysContact.0 = STRING:

    # Versus, lacking .0
    # $ snmpget -v2c -c public  192.168.10.21 SNMPv2-MIB::sysContact
    # SNMPv2-MIB::sysContact = No Such Instance currently exists at this OID

    if index is None:
        index = "0"
        oid = oid + ".0"
    new["snmp_oid"] = oid
    new["snmp_index"] = index
    new["snmp_mib"] = mib
    new["snmp_label"] = label

    datatype = get_datatype_name(mib, oid)
    new["snmp_datatype"] = datatype

    # Time to deal with description.
    if not line["description"]:
        description = get_description(mib, oid)
    elif line["description"] == line["name"]:
        description = get_description(mib, oid)
    else:
        description = line["description"]

    if not description:
        description = line["name"]
        FIXER.warning(
            "Useless description for (%s) == %s, fix manually",
            oid,
            description,
        )
    new["description"] = description.strip()

    units = line.get("units", "")
    if not units:
        new["units"] = get_units(mib, oid)

    for key in line.keys():
        if line[key] != new[key]:
            FIXER.info("%s changed:  %s => %s", key, line[key], new[key])
    return new


OK_EMPTY_FIELDS = ("units", "units_factor")


def check_single_line(
    line: Line,
    err_msg: Callable,
    keyparts: Set[str],
    names: Set[str],
    oids: Set[str],
) -> bool:
    """Check if a line in a CSV file is valid.

    We will try to resolve different parts of the CSV line as much as possible
    in order to test them for validity.

    """
    res = True

    for key in set(SNMP_CSV_ITEMS) - line.keys():
        res = False
        err_msg(f"Error: missing column {key}")

    for key in line:
        if key not in SNMP_CSV_ITEMS:
            err_msg(f"Warning: Extra column: {key}")

    for key, val in line.items():
        if val and val != val.strip():
            res = False
            err_msg(f"Error, field:{key} can be stripped.")

    for key, val in line.items():
        if not val:
            # Units can be empty.
            if key not in OK_EMPTY_FIELDS:
                res = False
                err_msg(f"Error, field:{key} is empty.")

    try:
        res = all(
            [
                check_keypart_okay(line, err_msg, keyparts),
                check_name_okay(line, err_msg, names),
                check_description_okay(line, err_msg),
                check_mib_okay(line, err_msg),
                check_index_okay(line, err_msg),
                check_label_okay(line, err_msg),
                check_oid_okay(line, err_msg, oids),
                check_datatype_okay(line, err_msg),
                check_units_okay(line, err_msg),
                check_units_factor_okay(line, err_msg),
            ]
        )
    except Exception:
        print("Error with line", line)
        raise

    return res


def check_keypart_okay(
    line: Line, err_msg: Callable, keyparts: Set[str]
) -> bool:
    """Check the line if the keypart is okay.

    Updates keyparts to ensure uniqueness.
    """
    res = True
    keypart = line.get("keypart", "")

    if not keypart:
        res = False
        err_msg("Error, empty keypart")
        # Error out early as to not confuse
        return res

    if keypart in keyparts:
        res = False
        err_msg(f"Error, Duplicate keypart: {keypart}")
    keyparts.add(keypart)

    if not valid_keypart(keypart):
        res = False
        err_msg(f"Error: Keypart '{keypart}' invalid according to validator")

    return res


def check_name_okay(line: Line, err_msg: Callable, names: Set[str]) -> bool:
    """Check the line if the name is okay.

    Will add the name to names to test for uniqueness.
    """
    res = True
    if "name" not in line:
        res = False
        err_msg("Error, Name absent")

    name = line.get("name", "")
    if not name:
        res = False
        err_msg("Error, Name empty")

    if name in names:
        res = False
        err_msg(f"Warning, Name used more than once: {name}")
    names.add(name)
    return res


def check_datatype_okay(line: Line, err_msg: Callable) -> bool:
    """Check line if the datatype is okay."""
    res = True
    if "snmp_datatype" not in line:
        res = False
        err_msg("Error, datatype missing absent")

    datatype = line.get("snmp_datatype", "")
    if not datatype:
        res = False
        err_msg("Error, datatype empty")

    if datatype not in VALIDATORS:
        res = False
        err_msg(f"Error, datatype: {datatype} has no validator.")

    snmp_oid = line.get("snmp_oid", "")
    if snmp_oid:
        resolved_datatype = get_datatype_name("", snmp_oid)
        if resolved_datatype != datatype:
            res = False
            err_msg(
                f"Error: Resolved datatype of {snmp_oid}"
                f"to {resolved_datatype} != {datatype}"
            )
    return res


def check_description_okay(line: Line, err_msg: Callable) -> bool:
    """Check line if the description is okay."""
    res = True
    if "description" not in line:
        res = False
        err_msg("Error, Description absent")

    description = line.get("description", "")
    if not description:
        res = False
        err_msg("Error, Description empty")

    name = line.get("name", "")
    if description == name:
        err_msg(f"Warning, description equals name: {description}")

    return res


def check_units_okay(line: Line, err_msg: Callable) -> bool:
    """Check line if the units is okay."""
    res = True
    if "units" not in line:
        res = False
        err_msg("Error, Units absent")

    snmp_oid = line.get("snmp_oid", "")
    if snmp_oid:
        snmp_units = get_units("", snmp_oid)
    else:
        snmp_units = ""

    units = line.get("units", "")
    if units and snmp_units:
        if units != snmp_units:
            if snmp_units in SENML_UNITS:
                err_msg(f"Units differs {units} != (MIB) {snmp_units}")

    if units and units not in SENML_UNITS:
        res = False
        err_msg(f"Unit {units} not in SENML_UNITS list")

    if snmp_units and not units:
        res = False
        err_msg(f"Error, Missing units where MIB has units: '{snmp_units}'")

    return res


def check_units_factor_okay(line: Line, err_msg: Callable) -> bool:
    """Check line if the units is okay."""
    res = True
    if "units_factor" not in line:
        res = False
        err_msg("Error, units_factor absent")

    units_factor = line.get("units_factor", "")
    if not units_factor:
        return res

    snmp_oid = line.get("snmp_oid", "")
    if not snmp_oid:
        # Always false, assume something else has a better error message
        return False
    datatype = get_datatype("", snmp_oid)
    if len(datatype.namedValues) != 0:
        items = dict(datatype.namedValues)
        res = False
        err_msg(
            f"Unit has factor {units_factor} while "
            f"type {datatype} is Enumeration of {items}"
        )

    try:
        val = decimal_string(units_factor)
        if val == 0:
            res = False
            err_msg(f"units_factor: {units_factor} must not be 0")
    except ArithmeticError:
        res = False
        err_msg(f"units_factor: {units_factor} not a valid Decimal")

    return res


def check_index_okay(line: Line, err_msg: Callable) -> bool:
    """Check line for an acceptable index."""
    res = True
    snmp_index = line.get("snmp_index", "")
    if not snmp_index:
        res = False
        err_msg("Missing snmp_index")

    if not valid_snmp_index(snmp_index):
        res = False
        err_msg(f"snmp_index doesn't validate: {snmp_index}")

    snmp_oid = line.get("snmp_oid", "")
    if snmp_oid:
        _, _, oid_index = resolve_names("", snmp_oid)
        if oid_index is not None:
            if oid_index != snmp_index:
                res = False
                err_msg(
                    f"Error:{snmp_index} mismatches OID resolved: {oid_index}"
                )

    if not snmp_oid.endswith(snmp_index):
        res = False
        err_msg(f"Error: OID {snmp_oid} should end with index: {snmp_index}")
    return res


def check_label_okay(line: Line, err_msg: Callable) -> bool:
    """Check line for an accetable label."""
    res = True
    snmp_label = line["snmp_label"]
    if not snmp_label:
        res = False
        err_msg("snmp_label is empty")
        return res

    snmp_mib = line.get("snmp_mib", "")
    if snmp_mib:
        _, resolved_label, resolved_index = resolve_names(snmp_mib, snmp_label)

        if resolved_index:
            res = False
            err_msg(f"Error, MIB::Label results in an index: {resolved_index}")

        if snmp_label != resolved_label:
            res = False
            err_msg(
                "Error, MIB::Label to Label mismatch "
                f"{snmp_label} != {resolved_label}"
            )

    snmp_oid = line.get("snmp_oid", "")
    if snmp_oid:
        _, resolved_label, _ = resolve_names("", snmp_oid)
        if snmp_label != resolved_label:
            res = False
            err_msg(
                f"Error, OID({snmp_oid}) to Label mismatch "
                f"{snmp_label} != {resolved_label}"
            )
    return res


def check_mib_okay(line: Line, err_msg: Callable) -> bool:
    """Check line for valid mib."""
    res = True

    # Start with the mib
    snmp_mib = line["snmp_mib"]
    if not snmp_mib:
        err_msg("MIB not mentioned")
        return False

    if not resolving_mib(snmp_mib):
        res = False
        err_msg(f"Error: MIB fails to load: {snmp_mib}")

    snmp_oid = line.get("snmp_oid", "")
    if snmp_oid:
        resolved_mib, _, _ = resolve_names("", snmp_oid)
        if resolved_mib != snmp_mib:
            res = False
            err_msg(
                f"Resolved OID({snmp_oid}) to "
                f"MIB({resolved_mib}) != {snmp_mib}"
            )
    return res


def check_oid_okay(line: Line, err_msg: Callable, oids: Set[str]) -> bool:
    """Check line for valid oid.

    Matches that it is unique against the set of oids.
    """
    snmp_oid = line.get("snmp_oid", "")
    res = True
    if not snmp_oid:
        res = False
        err_msg("Error, empty OID in field")
        # Exit early to avoid confusing errors
        return res

    if snmp_oid in oids:
        res = False
        err_msg(f"Error, already seen this OID: {snmp_oid}")
    oids.add(snmp_oid)

    if not valid_numeric_oid(snmp_oid):
        res = False
        err_msg(f"OID should be all numeric, not {snmp_oid}")

    snmp_index = line.get("snmp_index", "")

    if not snmp_oid.endswith(snmp_index):
        res = False
        err_msg(
            f"Error, OID: {snmp_oid} needs to end with the index {snmp_index}"
        )
    return res


def check_csv_content(fobj: TextIO) -> bool:
    """Parse an opened csv test its integrity."""
    result = True
    reader = csv.DictReader(fobj, fieldnames=None, delimiter=";")
    keyparts = set(RESERVED_KEYPARTS)
    names: Set[str] = set()
    oids: Set[str] = set()

    def err_msg(msg: str) -> None:
        """We don't have a logger or structlog due to embedded and others.

        This is just a wrapper for similar usecase.
        """
        err_template = "{filename}:{line_num}: {message}"
        out = err_template.format(
            filename=fobj.name, line_num=reader.line_num, message=msg
        )
        print(out)

    for line in reader:
        result &= check_single_line(
            line,
            err_msg=err_msg,
            keyparts=keyparts,
            names=names,
            oids=oids,
        )

    return result


def check_csv_file(fobj: TextIO) -> bool:
    """Check that a csv file is ok to our spec."""
    with reseek_file(fobj):
        header_ok = check_csv_header(fobj)

    with reseek_file(fobj):
        body_ok = check_csv_content(fobj)
    return all((header_ok, body_ok))


def fix_csvfile(file_path: pathlib.Path) -> None:
    """Fix a single CSV file as best as we can."""
    assert isinstance(file_path, pathlib.Path)
    backup_file = file_path.with_name(file_path.name + "~")
    # Create a new named temp file, so we can rename it afterwards
    try:
        with tempfile.NamedTemporaryFile(
            dir=file_path.parent, mode="w+t"
        ) as w_file:
            temppath = pathlib.Path(w_file.name)

            # Create a writer with our "known good" header (SNMP_CSV_ITEMS)
            writer = csv.DictWriter(
                w_file, fieldnames=SNMP_CSV_ITEMS, delimiter=";"
            )
            writer.writeheader()
            FIXER.info(
                "Fixing file %s, writing to temp %s, backup file: %s",
                file_path,
                temppath,
                backup_file,
            )
            # open our source file, iterate over it and write corrected
            # lines to the temp-file
            with file_path.open() as r_file:
                reader = csv.DictReader(r_file, fieldnames=None, delimiter=";")
                for line in reader:
                    corrected = fix_single_line(line)
                    writer.writerow(corrected)
            # Flush the file to make data consistent
            w_file.flush()

            # python3.8 introduces pathlib.unlink(missing_ok=True)
            if backup_file.exists():
                backup_file.unlink()

            # python3.8 introduces pathlib.Path.link().
            # Until then, use os.link()
            os.link(file_path, backup_file)
            # Rename the temppath to our file_path,
            # and return that to our caller
            temppath.rename(file_path)
    except FileNotFoundError:
        # File not found is an all-clear for this....
        pass
    FIXER.info("Fixed file %s", file_path)


def all_csvfiles() -> Iterable[pathlib.Path]:
    """List all our csv files, retruning a Path-like object for each."""
    data_path = pathlib.Path(__file__).parent / "data"
    yield from data_path.glob("*.csv")


def all_fix() -> Iterable[str]:
    """Parse all CSV files and tries to "fix" all fields.

    This re-writes the files in-place in the repository.
    """
    for path in all_csvfiles():
        with path.open(mode="r") as ro_file:
            should_change = not check_csv_file(ro_file)
        if should_change:
            yield path.stem
            fix_csvfile(path)


def all_kinds() -> Iterable[str]:
    """Return all kinds in our dataset."""
    for path in all_csvfiles():
        yield path.stem


# Should there be a "has_mibs"?
def list_mibs(fobj: IO[str]) -> Set[str]:
    """List all MIBs mentioned in our CSV files."""
    result = set()
    with reseek_file(fobj):
        reader = csv.DictReader(fobj, fieldnames=None, delimiter=";")
        for line in reader:
            mib = line["snmp_mib"]
            result.add(mib)
    return result


MIB_BLACKLIST = set(
    (
        # Blacklisted by mibbuilder.py
        "INET-ADDRESS-MIB",
        "PYSNMP-USM-MIB",
        "RFC-1212",
        "RFC-1215",
        "RFC1065-SMI",
        "RFC1155-SMI",
        "RFC1158-MIB",
        "RFC1213-MIB",
        "SNMP-FRAMEWORK-MIB",
        "SNMP-TARGET-MIB",
        "SNMPv2-CONF",
        "SNMPv2-SMI",
        "SNMPv2-TC",
        "SNMPv2-TM",
        "TRANSPORT-ADDRESS-MIB",
        # part of pysnmp in smi/mibs/*
        "__PYSNMP-USM-MIB",
        "__SNMP-FRAMEWORK-MIB",
        "__SNMP-MPD-MIB",
        "__SNMP-TARGET-MIB",
        "__SNMP-USER-BASED-SM-MIB",
        "__SNMPv2-MIB",
        "__SNMP-VIEW-BASED-ACM-MIB",
        "ASN1-ENUMERATION",
        "ASN1",
        "ASN1-REFINEMENT",
        "INET-ADDRESS-MIB",
        "PYSNMP-MIB",
        "PYSNMP-SOURCE-MIB",
        "PYSNMP-USM-MIB",
        "RFC1158-MIB",
        "RFC1213-MIB",
        "SNMP-COMMUNITY-MIB",
        "SNMP-FRAMEWORK-MIB",
        "SNMP-MPD-MIB",
        "SNMP-NOTIFICATION-MIB",
        "SNMP-PROXY-MIB",
        "SNMP-TARGET-MIB",
        "SNMP-USER-BASED-SM-3DES-MIB",
        "SNMP-USER-BASED-SM-MIB",
        "SNMP-USM-AES-MIB",
        "SNMP-USM-HMAC-SHA2-MIB",
        "SNMPv2-CONF",
        "SNMPv2-MIB",
        "SNMPv2-SMI",
        "SNMPv2-TC",
        "SNMPv2-TM",
        "SNMP-VIEW-BASED-ACM-MIB",
        "TRANSPORT-ADDRESS-MIB",
    )
)


def all_mibs() -> List[str]:
    """Return all mibs actually USED by our CSV-files."""
    listed_mibs: Set[str] = set()
    result = []
    builder, viewer = get_builder()
    for path in all_csvfiles():
        with path.open(mode="r") as ro_file:
            mibs = list_mibs(ro_file)
            listed_mibs = listed_mibs.union(mibs)

    # It could be an empty string
    listed_mibs = {x for x in listed_mibs if x}

    for mib in listed_mibs:
        try:
            builder.loadModule(mib)
        except MibLoadError:
            result.append(mib)
            continue

    # This iterates through all LOADED mibs, not just directly mentioned in our
    # CSV files.
    # This makes dependencies show up as well.
    mib = viewer.getFirstModuleName()
    while True:
        # The MIB_BLACKLIST is a list of internal or "standard" mibs that
        # should always exist.
        # These cannot be compiled, and should always be available, and thus
        # shouldn't be part of the "maintainance" output and such.
        if mib and mib not in MIB_BLACKLIST:
            result.append(mib)
        try:
            mib = viewer.getNextModuleName(mib)
        except SmiError:
            break

    return result


def all_check() -> Iterable[str]:
    """Check all CSV-files."""
    failed = []
    for fname in all_datafiles():
        if not fname.endswith(".csv"):
            # Not a CSV so we do not care
            continue
        yield fname
        with importlib_resources.open_text("snmp_lookup.data", fname) as fil:
            if not check_csv_file(fil):
                failed.append(fname)
    if failed:
        raise ValueError("Incomplete files", failed)


def main() -> None:
    """Maintainance commandline wrapper."""
    parser = argparse.ArgumentParser(description="SNMP self maintenance")
    parser.add_argument(
        "command",
        choices=["mibs", "kinds", "check", "fix"],
        default="mibs",
    )
    args = parser.parse_args()
    logging.basicConfig()
    RESOLVE.setLevel(logging.INFO)
    INDEX.setLevel(logging.INFO)
    FIXER.setLevel(logging.DEBUG)
    CHECK.setLevel(logging.DEBUG)

    if args.command == "mibs":
        for mib in all_mibs():
            print(mib)

    if args.command == "kinds":
        for kind in all_kinds():
            print(kind)

    if args.command == "check":
        for kind in all_check():
            print("checking: ", kind)

    if args.command == "fix":
        for kind in all_fix():
            print("fixing: ", kind)
