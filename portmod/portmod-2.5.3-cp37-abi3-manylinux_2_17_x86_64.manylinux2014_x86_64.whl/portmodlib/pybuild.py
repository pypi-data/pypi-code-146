# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

# Note: Some phase function descriptions have are derived from the
# Gentoo Package Manager Specification, version 7.
#   https://projects.gentoo.org/pms/7/pms.html
# This is licensed under the CC-BY-SA-3.0 License

import json
import lzma
import os
from pathlib import Path
from typing import Any, List, Optional, Set, Union

from .atom import Atom, FQAtom, QualifiedAtom, Version
from .source import Source
from .usestr import use_reduce


class BasePybuild:
    """
    Interface describing the Pybuild Type
    Only describes elements that are cached.
    This class cannot be used to install/uninstall mods
    """

    __file__ = __file__
    _PYBUILD_VER: int

    version: Version
    ATOM: FQAtom
    RDEPEND: str = ""
    DEPEND: str = ""
    SRC_URI: str = ""
    P: Atom
    PF: Atom
    PN: Atom
    CATEGORY: str
    PV: str
    PR: str
    PVR: str
    CPN: QualifiedAtom
    CP: QualifiedAtom
    REQUIRED_USE: str = ""
    REQUIRED_USE_EFFECTIVE: str = ""
    RESTRICT: str = ""
    PROPERTIES: str = ""
    IUSE_EFFECTIVE: Set[str] = set()
    IUSE: Set[str] = set()
    TEXTURE_SIZES: str = ""
    DESC: str = ""
    NAME: str = ""
    HOMEPAGE: str = ""
    LICENSE: str = ""
    KEYWORDS: str = ""
    FILE: str
    REPO: str
    INSTALLED: bool = False
    S: Optional[str] = None  # Primary directory during prepare and install operations:w
    PATCHES: str = ""
    # Phase functions defined by the pybuild (or superclasses other than Pybuild1/2)
    # Used to determine if a function should be run, as certain functions don't have any default
    # behaviour
    FUNCTIONS: List[str] = []
    # Only set in phase functions
    USE: Set[str]

    def get_use(self) -> Set[str]:
        """Returns the enabled use flags for the package"""
        return self.USE

    def valid_use(self, use: str) -> bool:
        """Returns true if the given flag is a valid use flag for this mod"""
        return use in self.IUSE_EFFECTIVE


class FullPybuild(BasePybuild):
    """Interface describing the Pybuild Type"""

    __file__ = __file__
    REPO_PATH: Optional[str]
    __pybuild__: str

    # Variables defined during the install/removal process
    A: List[Source]  # List of enabled sources
    D: str  # Destination directory where the mod is to be installed
    FILESDIR: str  # Path of the directory containing additional repository files
    ROOT: str  # Path of the installed directory of the mod
    T: str  # Path of temp directory
    UNFETCHED: List[Source]  # List of sources that need to be fetched
    USE: Set[str]  # Enabled use flags
    WORKDIR: str  # Path of the working directory

    # Note: declared as a string, but converted into a set during __init__
    IUSE: Union[Set[str], str] = ""  # type: ignore
    KEYWORDS = ""

    def __init__(self):
        self.FILE = self.__class__.__pybuild__

        category = Path(self.FILE).resolve().parent.parent.name
        # Note: type will be fixed later by the loader and will become an FQAtom
        self.ATOM = Atom(  # type: ignore
            "{}/{}".format(category, os.path.basename(self.FILE)[: -len(".pybuild")])
        )
        self.version = self.ATOM.version

        self.REPO_PATH = str(Path(self.FILE).resolve().parent.parent.parent)
        repo_name_path = os.path.join(self.REPO_PATH, "profiles", "repo_name")
        if os.path.exists(repo_name_path):
            with open(repo_name_path, "r") as repo_file:
                self.REPO = repo_file.readlines()[0].rstrip()
            self.ATOM = FQAtom("{}::{}".format(self.ATOM, self.REPO))

        self.P = Atom(self.ATOM.P)
        self.PN = Atom(self.ATOM.PN)
        self.PV = self.ATOM.PV
        self.PF = Atom(self.ATOM.PF)
        self.PR = self.ATOM.PR or "r0"
        self.CATEGORY = self.ATOM.C
        self.R = self.ATOM.R
        self.CP = QualifiedAtom(self.ATOM.CP)
        self.CPN = QualifiedAtom(self.ATOM.CPN)
        self.PVR = self.ATOM.PVR

        self.IUSE_EFFECTIVE = set()

        if isinstance(self.IUSE, str):
            self.IUSE = set(self.IUSE.split())
            self.IUSE_EFFECTIVE |= set([use.lstrip("+") for use in self.IUSE])
        else:
            raise TypeError("IUSE must be a space-separated list of use flags")

        if type(self.KEYWORDS) is str:
            self.KEYWORDS = set(self.KEYWORDS.split())  # type: ignore # pylint: disable=no-member
        else:
            raise TypeError("KEYWORDS must be a space-separated list of keywords")

        self.REQUIRED_USE_EFFECTIVE: str = self.REQUIRED_USE
        if type(self.TEXTURE_SIZES) is str:
            texture_sizes = use_reduce(self.TEXTURE_SIZES, matchall=True)
            texture_size_flags = [
                "texture_size_{}".format(size) for size in texture_sizes
            ]
            self.IUSE_EFFECTIVE |= set(texture_size_flags)
            if texture_size_flags:
                self.REQUIRED_USE_EFFECTIVE += (
                    " ^^ ( " + " ".join(texture_size_flags) + " )"
                )
        else:
            raise TypeError(
                "TEXTURE_SIZES must be a string containing a space separated list of "
                "texture sizes"
            )

    def pkg_nofetch(self):
        """
        The pkg_nofetch function is run when the fetch phase of an fetch-restricted
        package is run, and the relevant source files are not available. It should
        direct the user to download all relevant source files from their respective
        locations, with notes concerning licensing if applicable.

        ``pkg_nofetch`` must require no write access to any part of the filesystem.
        """

    def pkg_pretend(self):
        """
        May be used to carry out sanity checks early on in the install process

        Note that the default does nothing, and it will not even be executed unless defined.

        ``pkg_pretend`` is run separately from the main phase function sequence, and does not
        participate in any kind of environment saving. There is no guarantee that any of
        an package’s dependencies will be met at this stage, and no guarantee that the system
        state will not have changed substantially before the next phase is executed.

        ``pkg_pretend`` must not write to the filesystem and the initial working directory
        should not be expected to be consistent.
        """

    def src_unpack(self):
        """
        The ``src_unpack`` function extracts all of the package’s sources.

        The initial working directory must be ``self.WORKDIR``, and the default implementation
        used when the package lacks the src_unpack function shall behave as::

            self.unpack(self.A)
        """

    def src_prepare(self):
        """
        The src_prepare function can be used for post-unpack source preparation.

        The initial working directory is :py:attr:`Pybuild2.S`, falling back to
        :py:attr:`Pybuild2.WORKDIR` if the directory does not exist.

        The default implementation used when the package lacks
        the ``src_prepare`` function shall behave as::

            if self.PATCHES:
                for patch in use_reduce(self.PATCHES, self.USE, flat=True):
                    path = os.path.join(self.FILESDIR, patch)
                    apply_patch(path)
        """

    def src_install(self):
        """
        The src_install function installs the package’s content to a directory specified in :py:attr:`Pybuild2.D`.

        The initial working directory is :py:attr:`Pybuild2.S`, falling back to :py:attr:`Pybuild.WORKDIR`
        if the directory does not exist.

        The default implementation used when the package lacks the ``src_install`` function shall behave as::

            for pattern in self.DOCS:
                self.dodoc(pattern)
        """

    def pkg_prerm(self):
        """
        Function called immediately before package removal

        In Pybuild1, this function has full write permissions to ROOT.
        In Pybuild2 it only has read permissions.

        Note that the default does nothing, and it will not even be executed unless defined.
        """

    def pkg_postinst(self):
        """
        Function called immediately after package installation

        In Pybuild1, this function has full write permissions to ROOT.
        In Pybuild2 it only has read permissions.

        Note that the default does nothing, and it will not even be executed unless defined.
        """

    @staticmethod
    def execute(
        command: str, pipe_output: bool = False, pipe_error: bool = False
    ) -> Optional[str]:
        """Function pybuild files can use to execute native commands"""

    def validate(self) -> List[str]:
        """
        QA Checks pybuild structure. This has the same restrictions as code in the global
        package scope.

        returns:
            A list of error messages
        """
        return []


class FullInstalledPybuild(FullPybuild):
    """Interface describing the type of installed Pybuilds"""

    INSTALLED_USE: Set[str] = set()
    INSTALLED: bool = True
    INSTALLED_REBUILD_FILES: Optional[Any] = None


def get_installed_env(pkg: BasePybuild):
    environment = {}
    path = os.path.join(os.path.dirname(pkg.FILE), "environment.xz")

    if os.path.exists(path):
        environment_json = lzma.LZMAFile(path)
        try:
            environment = json.load(environment_json)
        except EOFError as e:
            raise RuntimeError(f"Failed to read {path}") from e
    return environment
