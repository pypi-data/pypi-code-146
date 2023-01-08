import logging.config

from spoor import config

logging.config.dictConfig(config.LOGGING_CONFIG)
logger = logging.getLogger(__package__)
