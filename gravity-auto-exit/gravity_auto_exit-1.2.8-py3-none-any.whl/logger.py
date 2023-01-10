""" Настройка логгера """

import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from gravity_auto_exit import settings as s

# get named logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create file handler
handler = TimedRotatingFileHandler(filename=s.sys_log_name,
                                   when='midnight',
                                   backupCount=15,
                                   encoding='utf-8',
                                   delay=False)

stream_handler = logging.StreamHandler()
# create formatter and add to han   dler
formatter = Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# add the handler to named logger
logger.addHandler(handler)
logger.addHandler(stream_handler)


# set the logging level
logger.setLevel(logging.DEBUG)