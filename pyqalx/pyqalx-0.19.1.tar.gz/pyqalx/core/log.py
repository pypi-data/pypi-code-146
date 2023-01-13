import logging
import sys
import traceback
from logging.handlers import RotatingFileHandler

from pyqalx.config import BotConfig, UserConfig
from pyqalx.core.errors import QalxError


# The prefix for all pyqalx log names
LOGGER_NAME_PREFIX = "pyqalx"


class QalxRotatingFileHandler(RotatingFileHandler):
    """
    We always force some defaults for a qalx log
    """

    def __init__(self, *args, **kwargs):
        # 10 MB
        kwargs["maxBytes"] = kwargs.get("maxBytes", 10 * 1024 * 1024)
        kwargs["backupCount"] = kwargs.get("backupCount", 10)
        kwargs["mode"] = kwargs.get("mode", "w")
        super(QalxRotatingFileHandler, self).__init__(*args, **kwargs)

    def rotate(self, *args, **kwargs):
        """
        Overridden in order to ignore permission errors.
        This could happen when multiple processes are accessing the same
        log file.  If this happens, rotation is suppressed until the lock
        is dropped.  The log files will exceed the "maxBytes" value but logging
        will continue normally.
        """
        try:
            super(QalxRotatingFileHandler, self).rotate(*args, **kwargs)
        except PermissionError:
            # PermissionError: Multiple processes writing to same file.  Only
            #                  likely on Windows
            pass


class QalxLogFormatter(logging.Formatter):
    """
    Sometimes our log messages contain extra data.  Use this formatter to allow
    all handlers to use the same format while also handling the potential extra
    data
    """

    def __init__(self, style="%", *args, **kwargs):
        kwargs[
            "fmt"
        ] = "%(asctime)s %(name)-12s %(levelname)-8s %(process)d %(message)s"
        super(QalxLogFormatter, self).__init__(*args, **kwargs)
        self.style = style
        self.original_style = self._style

    def format(self, record):
        dict_record = record.__dict__
        self._style = self.original_style
        if (
            "entity_type" in dict_record.keys()
            and "entity_guid" in dict_record.keys()
        ):
            existing_format = self._style._fmt
            # Typically this is added if a user decorated function encounters
            # an unhandled exception
            existing_format += (
                " Entity Type: `%(entity_type)s`"
                " Entity GUID: `%(entity_guid)s`"
            )
            self._style = logging._STYLES[self.style][0](existing_format)
        return super(QalxLogFormatter, self).format(record)


def configure_logging(name, filename, level):
    """
    Configures a log.  Loggers are tied directly to an instance of
    :class:`~pyqalx.core.session.QalxSession` or :class:`~pyqalx.bot.Worker`
    and should be accessed via `instance.log.<level>`.
    All pyqalx loggers are prefixed with `<LOGGER_NAME_PREFIX>`

    :param name: The name of the log
    :type name: str
    :param filename: The full filename for where the log should be saved
    :type filename: str
    :param level: The level of the log
    :type level: str
    :return: logging.getLogger()
    """
    name = f"{LOGGER_NAME_PREFIX}.{name}"
    if isinstance(level, str):
        # convert to proper log level
        level = level.upper()
    _log = logging.getLogger(name)
    if not _log.handlers:
        handler = QalxRotatingFileHandler(filename=filename)
        handler.setFormatter(QalxLogFormatter())
        handler.setLevel(level)
        _log.addHandler(handler)
    _log.setLevel(level)
    return _log


def session_logging_suffix(config):
    """
    Returns the suffix to use for QalxSession logging instances based
    on the config

    :param config: A subclass of :class:`~pyqalx.config.configs.Config`
    :type config: ~pyqalx.config.configs.Config
    :return: The key_prefix split.
             i.e. `user` for `QALX_USER_` and `bot` for `QALX_BOT_`
    """
    return config.key_prefix.split("_")[1].lower()


def get_logger():
    """
    For all the given configured loggers will try and get a user session log
    to log the unhandled exception to.  If there are multiple configured user
    sessions just grab the first one.  If there are no user sessions
    configured (i.e. the error occurred before QalxSession was instantiated)
    then return the root log
    """
    _loggers = [name for name in logging.root.manager.loggerDict]

    # Figures out which log to use.  Will use the `user session` log first
    # as this is most likely to exist, falling back to the `bot session` log,
    # and finally using the root log.
    for config_type in [UserConfig, BotConfig]:
        suffix = session_logging_suffix(config_type)
        loggers = list(
            filter(lambda x: f"{LOGGER_NAME_PREFIX}.{suffix}" in x, _loggers)
        )
        loggers.sort(key=lambda x: -len(x))
        if loggers:
            # A log has been found, stop trying to find one
            break
    logger_name = logging.root.name
    if loggers:
        logger_name = loggers[0]
    return logging.getLogger(logger_name)


def exception_hook(exc_type, exc_value, exc_traceback, extra=None, log=None):
    """
    We want to log any unhandled exception that occurs in pyqalx.  This
    includes `Qalx*` errors (i.e. because a user has misconfigured something)
    and also if they have made an error in one of their decorated functions
    (i.e. @bot.process).  This catches all errors and logs them and also
    prints out the traceback
    """
    # If no log (i.e. it's an error in the normal codebase) then figure out
    # which log to use
    log = log or get_logger()

    if issubclass(exc_type, QalxError):
        # Only handle `Qalx*` Errors.  We don't want to consume anything the
        # user has done wrong.  This will however handle issues with decorated
        # bot functions as these are caught in ~bot.Bot and handled as a
        # QalxError.  (i.e. if the user does `int('a')` in a bot function the
        # exception will be logged and raised here.)
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        log.error(
            msg="Qalx Exception:",
            exc_info=(exc_type, exc_value, exc_traceback),
            extra=extra,
        )

        traceback.print_exception(
            exc_type, exc_value, exc_traceback, chain=False
        )
    else:
        log.error(
            msg="Unhandled Exception:",
            exc_info=(exc_type, exc_value, exc_traceback),
            extra=extra,
        )

        # This is an exception elsewhere in the users codebase outside of qalx
        # or any bot function. We don't handle it.  Just reraise it for
        # the user to fix
        raise exc_type(exc_value)


sys.excepthook = exception_hook
