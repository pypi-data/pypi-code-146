"""
Top-level module scribe for wtforglib.

Classes:

    Scribe

Functions:

    None

Misc variables:

    LOG_LEVELS
"""


import logging
from logging.handlers import SysLogHandler
from types import MappingProxyType
from typing import List

LOG_LEVELS = MappingProxyType(
    {
        "crit": logging.CRITICAL,
        "error": logging.ERROR,
        "warn": logging.WARN,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    },
)


class Scribe(object):
    """
    A class to create a logging system interface.

    ...

    Attributes
    ----------
    logger : Any
    """

    def __init__(self, **kwargs) -> None:
        r"""Initialize a logging system interface.

        :param \**kwargs:
            See below

        :Keyword Arguments:
            * *level* (``str``) --
                one of: 'debug', 'info', 'warn', 'error', 'critical', default: 'info'
            * *logfn* (``str``) --
                file name of log file, default ""
            * *sylognm* (``str``) --
                annotation used in syslog to identfiy records, default ""
            * *screen* (``bool``) --
                flag specifyig whether to log to screen, default False
            * *name* (``str``) --
                unique identifier for this loggin instance, default "wtfscribe"
        """
        warnings: List[str] = []
        self.name = kwargs.get("name", "wtfscribe")
        level = kwargs.get("level", "info")
        self.logfn = kwargs.get("logfn", "")
        self.syslognm = kwargs.get("syslognm", "")
        screen = kwargs.get("screen", False)
        self.logger = logging.getLogger(self.name)

        if level not in LOG_LEVELS:
            self.log_level = logging.INFO
            warnings.append("Invalid log level '{0}' changed to 'info'".format(level))
        else:
            self.log_level = LOG_LEVELS[level]
        self.logger.setLevel(self.log_level)
        self.handlers_nbr = 0
        self._add_file_handler()
        self._add_syslog_handler()
        self._add_screen_handler(screen)
        for warning in warnings:
            self.logger.warning(warning)

    def _add_file_handler(self) -> bool:
        """Initialize a file log handler.

        Returns
        -------
        bool
        """
        if self.logfn:
            filelog = logging.FileHandler(filename=self.logfn)
            filelog.setLevel(self.log_level)
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s",
                "%Y-%m-%d %H:%M:%S",
            )
            filelog.setFormatter(formatter)
            self.logger.addHandler(filelog)
            self.handlers_nbr += 1
            return True
        return False

    def _add_syslog_handler(self) -> bool:
        """Initialize a syslog handler.

        Returns
        -------
        bool
        """
        if self.syslognm:
            syslog = SysLogHandler(address="/dev/log")
            syslog.setFormatter(
                logging.Formatter(
                    "[{0}] %(levelname)8s: %(message)s".format(self.syslognm),
                ),
            )
            # don't send debug to syslog
            syslog_level = (
                logging.INFO if self.log_level < logging.INFO else self.log_level
            )
            syslog.setLevel(syslog_level)
            self.logger.addHandler(syslog)
            self.handlers_nbr += 1
            return True
        return False

    def _add_screen_handler(self, screen: bool) -> bool:
        """
        Add a screen log handler.

        Parameters
        ----------
        screen : bool
            specify whether to log to screen

        Returns
        -------
        bool

        """
        if not self.handlers_nbr or screen:
            console = logging.StreamHandler()
            # set a format which is simpler for console use
            # tell the handler to use this format
            console.setFormatter(logging.Formatter("%(levelname)8s: %(message)s"))
            console.setLevel(self.log_level)
            self.logger.addHandler(console)
            self.handlers_nbr += 1
            return True
        return False
