import errno
import os

from wtforglib.kinds import Fspec


class ShellError(Exception):
    """Raised when subprocess resultcode not 0."""


def raise_filenotfound(filenm: Fspec) -> None:
    """Raises a FileNotFoundError execption for the given filenm.

    Parameters
    ----------
    filenm : Union[str,PathLike[str]]
        The yaml file to load

    Raises
    ------
    FileNotFoundError
        If fail_missing is True and filenm does not exist
    """
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), str(filenm))
