
import logging
import sys

DEFAULT_LOG_LEVEL = logging.INFO

# define formatters

# e.g.: 17:31:27 - arthurai - info message
LITE_FORMATTER = logging.Formatter('%(asctime)s - arthurai - %(message)s', "%H:%M:%S")
# e.g.: 2022-10-13 17:31:27,703 - arthurai.core.data_service - ERROR - error message
FULL_FORMATTER = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# adapted from https://stackoverflow.com/a/16066513
class InfoFilter(logging.Filter):
    """
    A logging filter to only log messages that are debug or info level (i.e. never log warning or error messages)
    """
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)


def initialize_logging():
    """Creates a parent 'arthurai' logger with a console output and INFO level.
    """
    # fetch logger and set default level
    arthur_logger = logging.getLogger("arthurai")
    arthur_logger.setLevel(DEFAULT_LOG_LEVEL)

    # create handlers

    # stderr handler always uses the full formatter and logs to the "standard error" stream: this shows up as red text
    #  in jupyter notebooks. it logs warning and error messages in this way
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(FULL_FORMATTER)

    # stdout handler by default uses the lite formatter and logs to the "standard out" stream: this shows up as regular
    #  text in jupyter notebooks. it logs debug and info messages, but the debug messages don't make it through the
    #  'arthurai' logger log level set at the top of this function in practice
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.addFilter(InfoFilter())
    stdout_handler.setFormatter(LITE_FORMATTER)

    # add handlers to logger
    arthur_logger.handlers = []
    arthur_logger.addHandler(stdout_handler)
    arthur_logger.addHandler(stderr_handler)


def _set_arthur_log_level(level: int):
    logging.getLogger("arthurai").setLevel(level)


def enable_debug_logging():
    """Enables debug logging for the arthurai package. Note that log messages may be dropped while this function is
     being executed.
    """
    # recreate single handler to output everything to stderr
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.DEBUG)
    stderr_handler.setFormatter(FULL_FORMATTER)

    # set new handler to be the only one
    logger = logging.getLogger("arthurai")
    logger.handlers = []
    logger.addHandler(stderr_handler)

    _set_arthur_log_level(logging.DEBUG)


def disable_debug_logging():
    """Disables debug logging for the arthurai package.  Note that log messages may be dropped while this function is
     being executed.
    """
    initialize_logging()
