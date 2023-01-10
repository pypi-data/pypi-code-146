# vim: ts=4 sts=4 sw=4 ft=python expandtab :
#
# Author: D.S. Ljugmark <spider@skuggor.se>, Modio AB
# SPDX-License-Identifier: AGPL-3.0-or-later
#
"""Helpers that stand alone or are used by both maintain and others."""

# 2020-11: ModioAB/agile#2024
# pylint 2.6.0 has an issue with decorators + susbcriptable.
# python 3.9 changed Optional and Union to be decorated classes.
# Remove after pylint > 2.6.0 is released.
# https://github.com/PyCQA/pylint/issues/3882

# pylint: disable=unsubscriptable-object

from contextlib import contextmanager
from typing import Tuple, Union, List, IO, AnyStr, Generator


__all__ = ["break_key", "oid_split", "reseek_file"]
IntOrStr = Union[str, int]


@contextmanager
def reseek_file(fobj: IO[AnyStr]) -> Generator[IO[AnyStr], None, None]:
    """Contextmanager that resets a file position between use."""
    pos = fobj.tell()
    yield fobj
    fobj.seek(pos)


def break_key(key: str) -> Tuple[str, str, str]:
    """Break an snmp key into parts."""
    if not key.startswith("snmp."):
        raise ValueError("Not an snmp key")

    if not key.count(".") >= 3:
        raise ValueError("Not enough key parts")

    _, name, kind, part = key.split(".", maxsplit=3)
    return kind, name, part


def oid_split(name: str) -> Tuple[IntOrStr, ...]:
    """Split an oid from text into a tuple, turning to integers as suitable."""
    res: List[IntOrStr] = []
    for part in name.split("."):
        if not part:
            continue
        if part.isnumeric():
            val = int(part)
            res.append(val)
        else:
            res.append(part)
    return tuple(res)
