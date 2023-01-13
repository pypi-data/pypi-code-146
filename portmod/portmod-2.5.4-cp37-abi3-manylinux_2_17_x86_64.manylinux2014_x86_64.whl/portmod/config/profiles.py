# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Module for interacting with the user's profile
and iterating over the various associated directories
"""

import os
from typing import List, Set, Tuple

from portmod.functools import prefix_aware_cache
from portmod.globals import env
from portmod.repo import get_repo_root
from portmodlib.atom import Atom
from portmodlib.parsers.list import read_list


def profile_link() -> str:
    return os.path.join(env.prefix().CONFIG_DIR, "profile")


def set_profile(path: str) -> None:
    os.makedirs(env.prefix().CONFIG_DIR, exist_ok=True)
    linkpath = profile_link()
    if os.path.lexists(linkpath):
        os.unlink(linkpath)
    os.symlink(path, linkpath)


def profile_exists() -> bool:
    return bool(env.PREFIX_NAME and os.path.exists(profile_link()))


def get_profile_path() -> str:
    """Returns the path to the profile directory"""
    profilepath = profile_link()
    if not os.path.exists(profilepath) or not os.path.islink(profilepath):
        raise FileNotFoundError(
            f"{profilepath} does not exist.\n"
            "Please choose a profile before attempting to install packages"
        )

    return os.path.realpath(os.readlink(profilepath))


def _profile_relative_path() -> Tuple[str, str]:
    """
    Splits the profile path into the profile base
    and a relative path within the profile directory
    """
    fullpath = get_profile_path()
    repo_root = get_repo_root(fullpath)
    if not repo_root:
        raise RuntimeError(
            "Profile symlinks must point to a path inside a repository profile directory!"
        )
    profile_root = os.path.join(repo_root, "profiles")
    return profile_root, os.path.relpath(fullpath, start=profile_root)


def get_profile_name() -> str:
    """
    Returns the name of the profile

    That is, the path, relative to the profiles directory
    """
    return get_profile_path().split("profiles")[-1].lstrip(os.path.sep)


@prefix_aware_cache
def profile_parents() -> List[str]:
    """
    Produces the paths of all the parent directories for the selected profile, in order
    """
    if not env.PREFIX_NAME:
        return []

    repo, first = _profile_relative_path()

    def get_parents(base: str, directory: str, encoding=None) -> List[str]:
        parentfile = os.path.join(base, directory, "parent")
        parents = []
        if os.path.exists(parentfile):
            for parent in read_list(parentfile, encoding=encoding):
                parentpath = os.path.normpath(os.path.join(directory, parent))
                parents.extend(get_parents(base, parentpath))
                parents.append(parentpath)

        return parents

    parents = [first]
    parents.extend(get_parents(repo, first, encoding="utf-8"))

    userpath = os.path.join(env.prefix().CONFIG_DIR, "profile.user")
    if os.path.exists(userpath):
        parents.append(userpath)
        parents.extend(get_parents(userpath, "."))

    return [os.path.join(repo, path) for path in parents]


def get_system() -> Set[Atom]:
    """Calculates the system set using the user's currently selected profile"""
    system: Set[Atom] = set()
    for parent in profile_parents():
        packages = os.path.join(parent, "packages")
        if os.path.exists(packages):
            system |= {
                Atom(mod.lstrip("*"))
                for mod in read_list(packages)
                if mod.startswith("*")
            }

    return system
