import os
from typing import Optional

from wtforglib.kinds import Fspec, StrAnyDict


class Options(object):
    """Class to manage opstions."""

    debug: int
    output: Fspec
    quiet: bool
    names_only: bool
    refresh: bool
    verbose: int
    test: bool
    errors: int

    def __init__(self, opts: Optional[StrAnyDict] = None):
        """Construct options class."""
        if opts is None:
            opts = {}
        self.debug = opts.get("debug", 0)
        self.output = str(opts.get("output", ""))
        self.quiet = opts.get("quiet", False)
        self.names_only = opts.get("names_only", False)
        self.refresh = opts.get("refresh", False)
        self.verbose = opts.get("verbose", 0)
        self.test = opts.get("test", False)
        self.errors = 0
        if self.test:
            print("created instance of class {0}".format(self.__class__.__name__))

    def isdebug(self) -> bool:
        """Return true if debug option > 0."""
        return self.debug > 0

    def isverbose(self) -> bool:
        """Return true if verbose option > 0."""
        return self.verbose > 0

    def istest(self) -> bool:
        """Return value of test option."""
        return self.test

    def trace(self, message: str, level: int = 1) -> None:
        """Trace message."""
        if self.test or self.debug >= level:
            print(message)

    def requires_super_user(self, prefix: str = "Specified action") -> None:
        """Require super user permission."""
        if os.geteuid() != 0:
            if not self.test:
                raise PermissionError(
                    "{0} requires super user priviledges.".format(prefix),
                )

    def _debug(self, message: str) -> None:
        """Debug message."""
        self.trace(message)

    def _verbose(self, message: str, level: int = 1) -> None:
        """Show message if verbose level exceeds threshold."""
        if self.test or self.verbose >= level:
            print(message)
