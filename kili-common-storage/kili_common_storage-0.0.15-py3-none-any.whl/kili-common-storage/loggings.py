import logging
import os


class Logger(object):
    def __init__(self):
        logging.getLogger("pika").setLevel(logging.WARNING)
        level = logging.INFO
        if os.environ.get('_DEBUG') == '1':
            level = logging.DEBUG
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level)
        self.logger.propagate = False
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(
            logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s"))
        self.logger.addHandler(handler)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


logger = Logger()
