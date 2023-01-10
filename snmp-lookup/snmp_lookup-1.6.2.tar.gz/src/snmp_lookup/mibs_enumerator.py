"""Helper, not used."""
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#

from typing import Sequence

try:
    # Python 3.7+ feature
    from importlib import resources as importlib_resources
except (AttributeError, ImportError):
    import importlib_resources  # type: ignore


MIBS = "snmp_lookup.mibs"


def all_mibs() -> Sequence[str]:
    """Iterate over all MIBS and return the MIB references."""
    result = set()
    for fname in importlib_resources.contents(MIBS):
        if not importlib_resources.is_resource(MIBS, fname):
            # not a file. Directory or similar
            continue
        if not fname.endswith(".py"):
            continue
        if fname in ("__init__.py", "index.py"):
            continue
        basename, _ = fname.rsplit(".", 1)
        result.add(basename)
    return [x for x in result if x]
