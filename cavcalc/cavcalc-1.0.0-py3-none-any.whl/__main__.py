import sys

from . import _SESSION
from ._main import main
from ._session import SessionType


def cli_entry():
    # Inform the back-end that we are now in CLI mode
    _SESSION.mode = SessionType.CLI

    # No argument specified, just default to help page
    if len(sys.argv) == 1:
        _SESSION.parser.print_help(sys.stderr)
        sys.exit(1)

    main()


if __name__ == "__main__":
    cli_entry()
