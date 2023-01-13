from .errors import CavCalcError


def quit_print(msg: str):
    """Prints `msg` to stdout and exits with code -1 if in CLI mode, otherwise
    raises a `CavCalcError` with the given `msg`."""
    from . import _SESSION

    if _SESSION.is_cli_mode:
        print("ERROR: " + msg)
        exit(-1)
    else:
        raise CavCalcError(msg)


def bug(msg: str):
    quit_print("Bug encountered! " + msg)
