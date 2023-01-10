from typing import Optional

from wtforglib.kinds import StrAnyDict

from pacwrap.yum import YumHandler


class DnfHandler(YumHandler):
    """Class to handle dnf package manager."""

    def __init__(self, opts: Optional[StrAnyDict] = None):
        """Creates a dnf package handler."""
        super().__init__(opts)
        self.pkgcmd = "dnf"
