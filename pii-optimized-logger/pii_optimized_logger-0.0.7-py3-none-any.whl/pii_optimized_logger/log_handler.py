import logging
import loguru
import os

#########################################

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Define one parameter to enable / disable the handler

disable_handler = os.environ.get('log_disable_handler', '0')
# Define one parameter to define the max len for each message

max_length = os.environ.get('log_max_length', '500')
max_length = int(max_length)


class LoguruInterceptHandler(logging.Handler):
    """Enable loguru logging."""

    def emit(self, record):

        try:
            level = logger.level(record.levelname).name
        except:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # process message
        message = record.getMessage()

        # truncate the message based on the len max value
        message = (message[:max_length]) if len(message) > max_length else message

        if disable_handler == "1":
            new_message = message
        else:
            new_message = ""
            words = message.split()
            for item in words:
                if len(item) >= 4:
                    item_masked = "**" + item[2:]
                elif len(message) >= 2:
                    item_masked = "**" + item[1:]
                new_message += item_masked + " "

        # Print log
        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            logging.getLevelName(level), new_message)



def create():

    new_handler = [LoguruInterceptHandler()]  # overwrite old handlers
    return new_handler
