# Copyright 2022 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

import os
from typing import Generator, Iterable, List, Optional, Set, Tuple, Union

from portmodlib.globals import local_mods, root
from portmodlib.pybuild import BasePybuild
from portmodlib.usestr import check_required_use


class File:
    """
    Represents important installed files and their metadata

    .. warning::
        This class has been deprecated as of Portmod 2.4.
        It will be removed in Portmod 3.0
    """

    def __init__(
        self,
        NAME: str,
        REQUIRED_USE: str = "",
        OVERRIDES: Union[str, List[str]] = [],
        **kwargs,
    ):
        """
        File objects also support a REQUIRED_USE variable, for , and an OVERRIDES variable for overriding other plugins in the load order.
        """
        self.__keys__: Set[str] = set()
        self.NAME: str = NAME
        """Name of the file relative to the root of the InstallDir"""
        self.REQUIRED_USE: str = REQUIRED_USE
        """
        Requirements for installing this file

        The default empty string is always satisfied.
        See Pybuild2.REQUIRED_USE for details on the syntax.
        """
        self.OVERRIDES: Union[str, List[str]] = OVERRIDES
        """
        A list of files which this overrides when sorting (if applicable).

        Can either be in the form of a string containing use-conditionals (note that
        this does not support files that contain spaces) or a list of files to override.
        Note that these overridden files are not considered masters and do not need to
        be present.

        For archives it determines the order in which the fallback archives will be
        searched during VFS lookups.
        """
        if REQUIRED_USE:
            self._add_kwarg("REQUIRED_USE", REQUIRED_USE)
        if OVERRIDES:
            self._add_kwarg("OVERRIDES", OVERRIDES)

        for key in kwargs:
            self._add_kwarg(key, kwargs[key])

    def _add_kwarg(self, key, value):
        self.__dict__[key] = value
        self.__keys__.add(key)

    def __repr__(self):
        return self.__str__()

    def __str__(self) -> str:
        kvps = []
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, str):
                kvps.append(f'{key}="{getattr(self, key)}"')
            else:
                kvps.append(f"{key}={getattr(self, key)}")

        separator = ""
        if kvps:
            separator = ", "
        return f'File("{self.NAME}"' + separator + ", ".join(kvps) + ")"

    def _to_cache(self):
        cache = {"NAME": self.NAME}
        for key in self.__keys__:
            cache[key] = getattr(self, key)

        cache["__type__"] = "File"
        return cache


class InstallDir:
    """
    Represents a directory in the Virtual File System

    Note that arbitrary arguments can be passed to the constructor, as
    repositories may make use of custom information.
    See the repository-level documentation for such information.

    .. warning::
        This class has been deprecated as of Portmod 2.4.
        It will be removed in Portmod 3.0
    """

    def __init__(
        self,
        PATH: str,
        REQUIRED_USE: str = "",
        PATCHDIR: str = ".",
        S: Optional[str] = None,
        WHITELIST: Optional[List[str]] = None,
        BLACKLIST: Optional[List[str]] = None,
        RENAME: Optional[str] = None,
        DATA_OVERRIDES: str = "",
        ARCHIVES: Iterable[File] = (),
        VFS: Optional[bool] = None,
        DOC: Iterable[str] = (),
        **kwargs,
    ):
        self.PATH: str = PATH
        """
        The path to the data directory that this InstallDir represents
        relative to the root of the archive it is contained within.
        """
        self.REQUIRED_USE: str = REQUIRED_USE
        """
        A list of use flags with the same format as the package's
        REQUIRED_USE variable which enable the InstallDir if satisfied.
        Defaults to an empty string that is always satisfied.
        """
        self.PATCHDIR: str = PATCHDIR
        """
        The destination path of the InstallDir within the package's directory.

        Defaults to ".", i.e. the root of the mod directory. If multiple InstallDirs
        share the same PATCHDIR they will be installed into the same directory in the
        order that they are defined in the INSTALL_DIRS list.
        Each unique PATCHDIR has its own entry in the VFS, and its own sorting rules
        """
        self.S: Optional[str] = S
        """
        The source directory corresponding to this InstallDir.

        Similar function to S for the entire pybuild, this determines which directory
        contains this InstallDir, and generally corresponds to the name of the source
        archive, minus extensions. This is required for packages that contain more
        than one source, but is automatically detected for those with only one source
        if it is not specified, and will first take the value of Pybuild2.S, then the
        source's file name without extension if the former was not defined.
        """
        self.WHITELIST: Optional[List[str]] = WHITELIST
        """
        If present, only installs files matching the patterns in this list.
        fnmatch-style globbing patterns (e.g. * and [a-z]) can be used
        """
        self.BLACKLIST: Optional[List[str]] = BLACKLIST
        """
        If present, does not install files matching the patterns in this list.
        fnmatch-style globbing patterns (e.g. * and [a-z]) can be used
        """
        self.RENAME: Optional[str] = RENAME
        """
        Destination path of this directory within the final directory.

        E.g.::

            InstallDir("foo/bar", PATCHDIR=".", RENAME="bar")

        Will install the contents of ``foo/bar`` (in the source) into the directory
        ``bar`` inside the package's installation directory (and also the VFS).
        """
        self.DATA_OVERRIDES: str = DATA_OVERRIDES
        """
        A list of packages that this InstallDir should override in the VFS

        This only has a different effect from Pybuild1.DATA_OVERRIDES if multiple PATCHDIRs
        are set, as it can define overrides for individual PATCHDIRS, while
        Pybuild1.DATA_OVERRIDES affects all PATCHDIRs.
        See Pybuild1.DATA_OVERRIDES for details of the syntax.
        """
        self.ARCHIVES: List[File] = list(ARCHIVES)
        """
        A list of File objects representing VFS archives.

        These will be searched, in order, during VFS file lookups if the file is not
        present in the package directories.
        """
        self.VFS: Optional[bool] = VFS
        """
        Whether or not this InstallDir gets added to the VFS

        Defaults to the value of the VFS variable in the profile configuration
        """
        self.DOC: List[str] = list(DOC)
        """
        A list of patterns matching documentation files within the package

        This documentation will be installed separately
        fnmatch-style globbing patterns (e.g. * and [a-z]) can be used.
        """
        self.__keys__: Set[str] = set()
        if ARCHIVES:
            self._add_kwarg("ARCHIVES", ARCHIVES)
        if PATCHDIR != ".":
            self._add_kwarg("PATCHDIR", PATCHDIR)
        for arg in [
            "DATA_OVERRIDES",
            "RENAME",
            "BLACKLIST",
            "WHITELIST",
            "S",
            "REQUIRED_USE",
        ]:
            if getattr(self, arg):
                self._add_kwarg(arg, getattr(self, arg))
        for key in kwargs:
            self._add_kwarg(key, kwargs[key])

    def _add_kwarg(self, key, value):
        if isinstance(value, list):
            new_value = []
            for item in value:
                if isinstance(item, dict) and item.get("__type__") == "File":
                    file = dict(item)
                    file.pop("__type__", None)
                    new_value.append(File(**file))
                else:
                    new_value.append(item)
            value = new_value

        self.__dict__[key] = value
        self.__keys__.add(key)

    def get_files(self):
        """Generator function yielding file subattributes of the installdir"""
        for key in self.__dict__:
            if isinstance(getattr(self, key), list):
                for item in getattr(self, key):
                    if isinstance(item, File):
                        yield item

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        kvps = []
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, str):
                kvps.append(f'{key}="{getattr(self, key)}"')
            else:
                kvps.append(f"{key}={getattr(self, key)}")

        separator = ""
        if kvps:
            separator = ", "
        return f'InstallDir("{self.PATH}"' + separator + ", ".join(kvps) + ")"

    def _to_cache(self):
        cache = {"PATH": self.PATH}
        for key in self.__keys__:
            value = getattr(self, key)
            if isinstance(value, list):
                new = []
                for item in value:
                    if isinstance(item, File):
                        new.append(item._to_cache())
                    else:
                        new.append(item)
                value = new
            cache[key] = value

        return cache


def get_directories(package: BasePybuild) -> Generator[InstallDir, None, None]:
    """
    Returns all enabled InstallDir objects in INSTALL_DIRS
    """
    assert package._PYBUILD_VER == 1
    for install_dir in getattr(package, "INSTALL_DIRS"):
        if check_required_use(
            install_dir.REQUIRED_USE, package.get_use(), package.valid_use
        ):
            yield install_dir


def get_files(
    package: BasePybuild, typ: str
) -> Generator[Tuple[InstallDir, File], None, None]:
    """
    Returns all enabled files and their directories
    """
    for install_dir in get_directories(package):
        if hasattr(install_dir, typ):
            for file in getattr(install_dir, typ):
                if check_required_use(
                    file.REQUIRED_USE, package.get_use(), package.valid_use
                ):
                    yield install_dir, file


# Note: This function will only work inside the sandbox, as otherwise INSTALL_DEST
# won't be an environment variable
def _get_install_dir_dest(pkg: BasePybuild):
    install_dir_dest = os.environ.get("INSTALL_DEST", ".")
    for attr in dir(pkg):
        if not attr.startswith("_") and isinstance(getattr(pkg, attr), str):
            install_dir_dest = install_dir_dest.replace(
                "{" + attr + "}", getattr(pkg, attr)
            )
    return os.path.normpath(install_dir_dest)


def get_dir_path(pkg: BasePybuild, install_dir: InstallDir) -> str:
    """Returns the installed path of the given InstallDir"""
    # Local dirs should be relative to LOCAL_MODS
    if "local" in pkg.PROPERTIES:
        path = os.path.normpath(os.path.join(local_mods(), pkg.PN))
    else:
        path = os.path.normpath(
            os.path.join(root(), _get_install_dir_dest(pkg), install_dir.PATCHDIR)
        )
    if os.path.islink(path):
        return os.readlink(path)
    else:
        return path


def get_file_path(pkg: BasePybuild, install_dir: InstallDir, esp: File) -> str:
    return os.path.join(get_dir_path(pkg, install_dir), esp.NAME)
