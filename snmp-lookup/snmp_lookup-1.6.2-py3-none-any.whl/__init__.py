# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""The main library entrypoint is pretty empty.

Two selftest routines right now. The rest should all use the sub-modules.
"""

import argparse
from .selftests import test_import_looks_ok
from .selftests import run_selftest

from .validators import valid_name
from .validators import valid_kind
from .validators import valid_key
from .validators import valid_numeric_oid
from .validators import get_validator

from .kind import get_point
from .kind import get_snmp_type
from .kind import get_kind
from .kind import get_points

assert callable(get_kind)
assert callable(get_point)
assert callable(get_snmp_type)

assert callable(valid_name)
assert callable(valid_kind)
assert callable(valid_key)
assert callable(valid_numeric_oid)
assert callable(get_validator)

__all__ = [
    "selftest",
    "valid_numeric_oid",
    "valid_key",
    "valid_kind",
    "valid_name",
    "get_point",
    "get_points",
    "get_validator",
    "get_snmp_type",
]


def selftest() -> None:
    """Self-test routine."""
    parser = argparse.ArgumentParser(
        description="snmp_lookup self test routines"
    )
    parser.add_argument("--pysnmp", action="store_true")
    args = parser.parse_args()

    if args.pysnmp:
        test_import_looks_ok()
    run_selftest()
    print("All ok")


if __name__ == "__main__":
    selftest()
