#!/usr/bin/env python
import sys

from .version import __version__

__copyright__ = "Copyright (C) 2022,2023 Hiroshi Miura"


if __name__ == "__main__":
    from . import launcher
    sys.exit(launcher.main())
