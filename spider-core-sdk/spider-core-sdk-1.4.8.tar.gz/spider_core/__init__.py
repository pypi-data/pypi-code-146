import logging

logger = logging.getLogger(__name__)
null = logging.NullHandler()
logger.addHandler(null)
