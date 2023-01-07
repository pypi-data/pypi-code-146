__doc__ = """
JSGFToolsLeyzer module - Classes and methods to define and execute parsing grammars
=============================================================================
"""
from typing import NamedTuple


class version_info(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: str
    serial: int

    @property
    def __version__(self):
        return (
            f"{self.major}.{self.minor}.{self.micro}"
            + (
                f"{'r' if self.releaselevel[0] == 'c' else ''}{self.releaselevel[0]}{self.serial}",
                "",
            )[self.releaselevel == "final"]
        )

    def __str__(self):
        return f"{__name__} {self.__version__} / {__version_time__}"

    def __repr__(self):
        return f"{__name__}.{type(self).__name__}({', '.join('{}={!r}'.format(*nv) for nv in zip(self._fields, self))})"


__version_info__ = version_info(0, 2, 0, "final", 0)
__version_time__ = "18 Dec 2022 13:30 UTC"
__version__ = __version_info__.__version__
__versionTime__ = __version_time__
__author__ = "cartesinus <msowansk@gmail.com>"

from .grammar import *
from .parser import *
from .utils import *
