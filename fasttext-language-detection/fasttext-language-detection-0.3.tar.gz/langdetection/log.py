import logging

log_format = '[%(asctime)-15s] %(levelname)s %(message)s'
logging.basicConfig(format=log_format)
logger = logging.getLogger('lang-detector')
logger.setLevel(logging.DEBUG)
