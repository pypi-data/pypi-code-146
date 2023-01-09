import traceback

import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt='iso'),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
)

class Logger:

    def __init__(self):

        self.log = structlog.get_logger()

    def parse(self, message):
        """
        Parses the message to a dict. This allows for ES to index it properly
        """

        if isinstance(message, str):
            message = {
                'text': message,
            }

        return message

    def critical(self, message):
        self.log.critical(self.parse(message))

    def debug(self, message):
        self.log.debug(self.parse(message))

    def error(self, message):
        self.log.error(self.parse(message))

    def fatal(self, message):
        self.log.fatal(self.parse(message))

    def info(self, message):
        self.log.info(self.parse(message))

    def msg(self, message):
        self.log.msg(self.parse(message))

    def warning(self, message):
        self.log.warning(self.parse(message))

    def metric(self, name, value):
        self.log.msg({'metric': name, 'value': value})

    def bind(self, **parameters):
        self.log = self.log.bind(**parameters)

    def unbind(self, *keys):
        self.log = self.log.unbind(keys)

    def exception(self, exc):

        tb = traceback.format_exc().replace('\n', ';;')

        self.log.fatal({'exception': exc, 'traceback': tb})
