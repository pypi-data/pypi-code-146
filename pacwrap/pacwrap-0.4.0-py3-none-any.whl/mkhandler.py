import re
from typing import Tuple

import distro
from cmp_version import cmp_version
from wtforglib.kinds import StrAnyDict

from pacwrap.apt import AptHandler
from pacwrap.dnf import DnfHandler
from pacwrap.pacman import PacmanHandler
from pacwrap.pkgmgr import PackageHandler
from pacwrap.yum import YumHandler


def get_osinfo(options: StrAnyDict) -> Tuple[str, str, str]:
    """Returns distro data sanely."""
    osid: str = distro.id()
    oslike: str = distro.like()
    osvers: str = distro.version()
    otest = options.get("test")
    if otest:
        osid = options.get("osid", osid)
        oslike = options.get("oslike", oslike)
        osvers = options.get("osvers", osvers)
    if osid in {"debian", "pop"}:
        oslike = "debian"
    elif osid in {"fedora", "rocky"}:
        oslike = "rhel"
    elif osid in {"arch", "manjaro"}:
        oslike = "arch"
    return (osid, oslike, osvers)


def create_rhel_handler(options: StrAnyDict, osid: str, osvers) -> PackageHandler:
    """Returns package handler for redhat family."""
    if osid == "fedora":
        threshold_ver = "22"
    else:
        threshold_ver = "8"
    if cmp_version(osvers, threshold_ver) < 0:
        return YumHandler(options)
    return DnfHandler(options)


def create_handler(options: StrAnyDict) -> PackageHandler:
    """Returns package handler for distro."""
    osid, oslike, osvers = get_osinfo(options)

    phandler: PackageHandler

    if oslike == "arch":
        phandler = PacmanHandler(options)
    elif oslike == "debian":
        phandler = AptHandler(options)
    elif re.search("rhel", oslike):
        phandler = create_rhel_handler(options, osid, osvers)
    else:
        raise ValueError("Unsupported distro like => {0}".format(oslike))
    return phandler
