# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Various utility functions
"""

from collections import namedtuple
from typing import Any, Iterable, List, Optional, Tuple

from portmod.config.license import has_eula, is_license_accepted
from portmod.repo.keywords import accepts, accepts_testing, get_keywords
from portmodlib.atom import QualifiedAtom, version_gt

from .globals import env
from .pybuild import Pybuild

KeywordDep = namedtuple("KeywordDep", ["atom", "keyword", "masked"])
LicenseDep = namedtuple("LicenseDep", ["atom", "license", "is_eula", "repo"])


def is_keyword_masked(arch: str, keywords: Iterable[str]):
    return "-" + arch in keywords or (
        "-*" in keywords and arch not in keywords and "~" + arch not in keywords
    )


def get_keyword_dep(package: Pybuild) -> Optional[KeywordDep]:
    if not accepts(get_keywords(package.ATOM), package.KEYWORDS):
        arch = env.prefix().ARCH
        if accepts_testing(arch, package.KEYWORDS):
            return KeywordDep(QualifiedAtom(package.ATOM.CP), "~" + arch, False)
        return KeywordDep(
            QualifiedAtom("=" + package.ATOM.CP),
            "**",
            is_keyword_masked(arch, package.KEYWORDS),
        )
    return None


def select_package(packages: Iterable[Pybuild]) -> Tuple[Pybuild, Any]:
    """
    Chooses a mod version based on keywords and accepts it if the license is accepted
    """
    if not packages:
        raise Exception("Cannot select mod from empty modlist")

    filtered = list(
        filter(lambda pkg: accepts(get_keywords(pkg.ATOM), pkg.KEYWORDS), packages)
    )

    keyword = None

    if filtered:
        mod = max(filtered, key=lambda pkg: pkg.version)
    else:
        arch = env.prefix().ARCH
        # No mods were accepted. Choose the best version and add the keyword
        # as a requirement for it to be installed
        unstable = list(
            filter(lambda mod: accepts_testing(arch, mod.KEYWORDS), packages)
        )
        if unstable:
            mod = max(unstable, key=lambda pkg: pkg.version)
            keyword = "~" + arch
        else:
            # There was no mod that would be accepted by enabling testing.
            # Try enabling unstable
            mod = max(packages, key=lambda pkg: pkg.version)
            keyword = "**"

    deps: List[Any] = []
    if not is_license_accepted(mod, mod.get_use()):
        deps.append(LicenseDep(mod.CPN, mod.LICENSE, has_eula(mod), mod.REPO))
    if keyword is not None:
        deps.append(
            KeywordDep(
                QualifiedAtom("=" + mod.ATOM.CPF),
                keyword,
                is_keyword_masked(env.prefix().ARCH, mod.KEYWORDS),
            )
        )

    return (mod, deps or None)


def get_max_version(versions: Iterable[str]) -> Optional[str]:
    """
    Returns the largest version in the given list

    Version should be a valid version according to PMS section 3.2,
    optionally follwed by a revision

    Returns None if the version list is empty

    .. warning::
        Deprecated and will be removed in portmod 2.6
    """
    newest = None
    for version in versions:
        if newest is None or version_gt(version, newest):
            newest = version
    return newest


def get_newest(packages: Iterable[Pybuild]) -> Pybuild:
    """
    Returns the newest mod in the given list based on version

    .. warning::
        Deprecated and will be removed in portmod 2.6
    """
    return max(packages, key=lambda pkg: pkg.version)


def sort_by_version(packages: Iterable[Pybuild]) -> List[Pybuild]:
    """
    Sorts the given packages in order of version

    .. warning::
        Deprecated and will be removed in portmod 2.6
    """
    return sorted(packages, key=lambda pkg: pkg.version)
