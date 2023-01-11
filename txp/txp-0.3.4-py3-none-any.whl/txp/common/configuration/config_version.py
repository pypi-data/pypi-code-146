"""This module contains functions that helps to deal with the
configuration version handling"""
import re
from typing import Tuple

"""A preliminar configuration version number is given by a string with the following
regular expression."""
_preliminar_version_rgx = re.compile(r"([0-9]+)\.([0-9]+)")


_normal_version_rgx = re.compile(r"([0-9]+)")


def is_preliminary_version(version: str) -> bool:
    return _preliminar_version_rgx.match(version) is not None


def is_normal_version(version: str) -> bool:
    return _normal_version_rgx.match(version) is not None


def get_next_preliminary_version(version: str) -> str:
    if is_preliminary_version(version):
        groups = list(_preliminar_version_rgx.match(version).groups())
        suffix_number = int(groups[1]) + 1
        return groups[0] + "." + str(suffix_number)

    else:
        return version + ".1"


def get_next_normal_version(version: str) -> str:
    if is_preliminary_version(version):
        groups = list(_preliminar_version_rgx.match(version).groups())
        new_version_number = int(groups[0]) + 1
        return str(new_version_number)
    else:
        new_number = int(version) + 1
        return str(new_number)
