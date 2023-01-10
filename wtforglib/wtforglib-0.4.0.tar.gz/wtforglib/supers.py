"""Top-level module for wtforglib Library."""

# vim:ft=py noqa: E800

from os import geteuid


def issuper() -> bool:
    """Return True/False depending on process euid.

    Returns
    -------
        bool : true if process euid is 0
    """
    return geteuid() == 0


def requires_super_user(prefix: str = "Specified action") -> None:
    """Raises exception if process isn't euid 0.

    Parameters
    ----------
    prefix : str
        Text to prefix to exception message

    Raises
    ------
    PermissionError
        if process euid is not 0
    """
    if not issuper():  # pragma no cover
        raise PermissionError("{0} requires super user priviledges!".format(prefix))
