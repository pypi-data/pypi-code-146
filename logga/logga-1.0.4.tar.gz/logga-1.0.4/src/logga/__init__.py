"""Custom logger based on content from
[Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html).

Configuration file for the logging module can be provided in the following locations:

- A place named by the environment variable `LOGGA_CONF`
- Current directory: `./log.conf`
- User's home directory: `~$USER/log.conf`

If not found, fallback is Logga's own configuration.

This arrangement is analogous to "rc" files. for example, "bashrc", "vimrc", etc.

"""
from typing import List, Optional, Text
import datetime
import inspect
import logging
import logging.config
import os
import pathlib


def locations() -> List[Text]:
    """Provide logging configuration directory locations in order of precedence.

    Returns:
        A list of locations as a set of strings that represent the directory location of the `log.conf` file.

    """
    def items():
        return (os.environ.get('LOGGA_CONF'),
                os.getcwd(),
                pathlib.Path.home())

    return items()


def get_logger_name() -> Optional[Text]:
    """Identify logger name to target handlers.

    The calling script will be the outermost call in the stack. Parse the
    resulting frame to get the name of the script.

    `<stdin>` is a special case that will explicitly return `None`

    Returns:
        The logger name as a string, or `None`.

    """
    _name = os.path.basename(inspect.stack()[-1][1])
    if _name == '<stdin>':
        _name = None

    return _name


def source_logger_config() -> Text:
    """Source logger config.

    Will attempt to parse a `log.conf` file to feed into `logging.config.fileConfig`. Will also
    determine the name of the calling script/module and associate that logger name with the
    `log.conf`.

    Returns:
        The name of the logger. Fallback, if no `log.conf` files are found is the `logga` logger.

    """
    config_found = False
    for loc in locations():
        if loc is None:
            continue

        try:
            with open(os.path.join(loc, 'log.conf'), encoding='utf-8') as _fh:
                logging.config.fileConfig(_fh)
                config_found = True
                break
        except IOError:
            # Not a bad thing if the open failed. Just means that the log
            # source does not exist.
            continue

    logger_name: Optional[Text] = get_logger_name()

    if not config_found:
        logger_name = 'logga'

        # If we've fallen through to here, then use Logga's own config.
        config_path = os.path.join(pathlib.Path(__file__).resolve().parents[0],
                                   'config',
                                  'log.conf')
        with open(config_path, encoding='utf-8') as _fh:
            logging.config.fileConfig(_fh)

    return logger_name


log = logging.getLogger(source_logger_config())


if log.name is not None:
    # Contain logging to the configured handler only (not console).
    log.propagate = False


def set_console():
    """Drop back to the root logger handler. This is typically the console.

    This can be used to override the logging file output stream and send
    log messages to the console. For example, consider the following
    code that has a `log.conf`` that writes to the log file `my.log`:

    ```
    from logga import log, set_console

    set_console()
    log.debug('Log from inside my Python module')
    ```

    The `set_console()` call will force the log message to write
    ``Log from inside my Python module`` to the console.

    """
    def default_console_config() -> logging.StreamHandler:
        """Default console config that can be used as a fallback.

        Returns a logging.StreamHandler configured with a simple format.

        """
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(asctime)s [%(levelname)s]:: %(message)s")
        console_handler.setFormatter(console_formatter)

        return console_handler

    for hdlr in log.handlers:
        log.removeHandler(hdlr)

    log.propagate = False

    log.addHandler(default_console_config())
    log.level = logging.NOTSET


def set_log_level(level: Text = 'INFO'):
    """Set the lower threshold of logged message level. Level defaults to `INFO``.
    All default log levels are supported (in order of severity):

    - `CRITICAL`
    - `ERROR`
    - `WARNING`
    - `INFO`
    - `DEBUG`
    - `NOTSET`

    Example:

    ```
    >>> from logga import log, set_log_level
    >>> log.info('This INFO message should display')
    2023-01-09 10:29:04 logga [INFO]: This INFO message should display
    >>> log.debug('Not this DEBUG')
    >>> set_log_level(level='DEBUG')
    >>> log.debug('DEBUG is now good to go')
    2023-01-09 10:30:15 logga [DEBUG]: DEBUG is now good to go
    ```

    Parameters:
        level: the lower log level threshold. All log levels, including and above this level in
               serverity, will be logged

    """
    level_map = {
        'CRITICAL': logging.INFO,
        'ERROR': logging.INFO,
        'WARNING': logging.INFO,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG,
        'NOTSET': logging.DEBUG,
    }

    log.setLevel(level_map[level])


def suppress_logging():
    """Provides an overriding (to level `CRITICAL`) suppression mechanism
    for all loggers which takes precedence over the logger`s own level.

    This function can be useful when the need arises to temporarily throttle logging output down
    across the whole application.

    Technically, this function will disable all logging calls below severity level `CRITICAL`. For example:

    ```
    >>> from logga import log, suppress_logging
    >>> log.info('This INFO message should display')
    2023-01-09 10:33:43 logga [INFO]: This INFO message should display
    >>> suppress_logging()
    >>> log.info('This INFO message should NOT display')
    >>> log.critical('But CRITICAL messages will get through')
    2023-01-09 10:36:17 logga [CRITICAL]: But CRITICAL messages will get through
    ```
    """
    logging.disable(logging.ERROR)


def autolog(message):
    """Automatically log the current function details.

    Used interchangeably with the `log` handler object. Handy for
    for verbose messaging during development by adding more verbose detail
    to the logging message, such as the calling function/method name
    and line number that raised the log call. Will only work at the `DEBUG` level:

    ```
    >>> from logga import autolog, log, set_log_level
    >>> set_log_level('DEBUG')
    >>> autolog('Verbose')
    2023-01-09 10:46:12 logga [DEBUG]: Verbose: <module> in <stdin>:1
    >>> log.debug('DEBUG message')
    2023-01-09 10:47:11 logga [DEBUG]: DEBUG message
    >>> autolog('DEBUG message')
    >>> 2023-01-09 10:47:34 logga [DEBUG]: DEBUG message: <module> in <stdin>:1
    ```

    Parameters:
        message: the log message to display

    """
    if log.isEnabledFor(logging.DEBUG):
        # Get the previous frame in the stack.
        # Otherwise it would be this function!!!
        frame = inspect.currentframe().f_back.f_code
        lineno = inspect.currentframe().f_back.f_lineno

        # Dump the message function details to the log.
        log.debug('%s: %s in %s:%i', message, frame.co_name, frame.co_filename, lineno)
