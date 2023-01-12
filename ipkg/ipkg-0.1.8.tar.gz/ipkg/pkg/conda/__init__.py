from pathlib import Path

from .. import OPT

NAME = "conda"
DEFAULT_PREFIX: Path = OPT / NAME
HELP_PREFIX = "Installation prefix/path."
