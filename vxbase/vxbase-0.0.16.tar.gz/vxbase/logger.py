import logging
import logging.handlers


def setup_logger(name='vxbase', level=logging.DEBUG, log_file=None):
    """Configures a logger, setting the level and a stream handler by default.
    If a log file name is passed, a file handler is also created.

    By default, it configures the 'vxbase' logger, so the config applies
    automatically to every other logger that belongs to a submodule.

    Important note: To avoid multiple configurations or overriding other loggers,
    the loggers should be called using 'logging.getLogger(__name__)', so the
    logger is named like the file where is being used. This also facilitates that
    every logger inside the 'deployv' module gets the correct parent settings.

    This function returns the configured logger, but it should be used to
    configure the parent logger ('vxbase') and only use a child logger from
    another module.
    """
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(level)
    logger.handlers = []
    formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)-5s - "
                                      "%(name)s.%(module)s.%(funcName)s - %(message)s")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
