import logging
import sys


def configure_logger(logger: logging.Logger) -> None:
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)-12s: %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.DEBUG)

    def stdout_handler_filter(rec: logging.LogRecord):
        return False if rec.levelno >= logging.WARNING else True

    stdout_handler.filter = stdout_handler_filter

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.WARNING)

    logger.addHandler(stdout_handler)
    logger.addHandler(stderr_handler)
    logger.setLevel(level=logging.INFO)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    configure_logger(logger)
    return logger


class LoggingMixin(object):
    """ Convenience super-class to have a logger
    configured with the class name """

    @property
    def log(self) -> logging.Logger:
        try:
            return self._log
        except AttributeError:
            logger = logging.getLogger(
                self.__class__.__module__ + '.' + self.__class__.__name__)
            configure_logger(logger)

            self._log = logger
            return self._log


class LoggingMeta(type):
    """ Convenience metaclass to have a logger
    configured with the class name """

    def __new__(mcs, name, bases, class_dict):
        logger = logging.getLogger(
            class_dict['__module__'] + '.' + name)
        configure_logger(logger)

        class_dict['log'] = logger

        cls = type.__new__(mcs, name, bases, class_dict)
        return cls
