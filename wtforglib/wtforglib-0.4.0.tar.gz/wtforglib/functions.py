"""Top-level module for wtforglib Library."""

import subprocess  # noqa: S404
from typing import ClassVar

from wtforglib.errors import ShellError


class WtfSingleton(object):
    """Singleton class."""

    dn: ClassVar[str] = ""
    hn: ClassVar[str] = ""

    def __new__(cls):  # pragma no cover
        """Creates new singleton if one does not exist."""
        if not hasattr(cls, "instance"):  # noqa: WPS421
            cls.instance = super(WtfSingleton, cls).__new__(cls)  # noqa: WPS608
        return cls.instance


def domainname(test: bool = False) -> str:  # noqa: WPS605
    """Retuns hosts domainname.

    Parameters
    ----------
    test : bool Optional
        Default False, when true return example.com

    Returns
    -------
    str
        domainname

    Raises
    ------
    ShellError
        if subprocess returncode is not 0
    """
    if not WtfSingleton.dn:
        sp_result = subprocess.run(
            ["hostname", "-d"],
            capture_output=True,
            encoding="utf8",
        )
        if sp_result.returncode != 0:  # pragma no cover
            raise ShellError("Failed to determine host's domainname")
        if test:
            WtfSingleton.dn = "example.com"
        else:  # pragma no cover
            WtfSingleton.dn = sp_result.stdout.rstrip()
    return WtfSingleton.dn


def hostname(test: bool = False) -> str:  # noqa: WPS605
    """Retuns hosts hostname.

    Parameters
    ----------
    test : bool Optional
        Default False, when true return nombre

    Returns
    -------
    str
        hostname

    Raises
    ------
    ShellError
        if subprocess returncode is not 0
    """
    if not WtfSingleton.hn:
        sp_result = subprocess.run(
            ["hostname"],
            capture_output=True,
            encoding="utf8",
        )
        if sp_result.returncode != 0:  # pragma no cover
            raise ShellError("Failed to determine hostname")
        if test:
            WtfSingleton.hn = "nombre"
        else:  # pragma no cover
            WtfSingleton.hn = sp_result.stdout.rstrip()
    return WtfSingleton.hn


def strtobool(rts: str) -> bool:
    """Covert string rts to boolean."""
    return rts.lower() in {"true", "1", "t", "y", "yes"}
