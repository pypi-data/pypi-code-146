"""Mainly data containing our header implementations for csv."""
import csv
from typing import TextIO, Iterator

import importlib_resources as resources


__all__ = ["SNMP_CSV_ITEMS", "check_csv_header", "all_datafiles"]

SNMP_CSV_ITEMS = [
    "snmp_mib",
    "snmp_label",
    "snmp_index",
    "snmp_oid",
    "snmp_datatype",
    "keypart",
    "name",
    "units",
    "units_factor",
    "description",
]


def check_csv_header(fobj: TextIO) -> bool:
    """Test that the csv fíle has the correct header."""
    reader = csv.DictReader(fobj, fieldnames=None, delimiter=";")
    # Read the file, DictReader will parse the header automatically, so we
    # compare the parsed result with our expectation of reality
    next(reader)
    return reader.fieldnames == SNMP_CSV_ITEMS


def all_datafiles() -> Iterator[str]:
    """Iterate over all datafiles, returning their filenames."""
    iterdir = resources.files("snmp_lookup.data").iterdir()
    files = (f.name for f in iterdir if f.is_file())
    for fname in files:
        if fname.endswith(".py"):
            # Python files we ignore
            continue

        yield fname
