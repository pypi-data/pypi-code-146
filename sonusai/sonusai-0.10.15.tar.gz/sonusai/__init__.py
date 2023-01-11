import logging
from os.path import dirname

from pkg_resources import get_distribution

__version__ = get_distribution('sonusai').version
BASEDIR = dirname(__file__)

# create logger
logger = logging.getLogger('sonusai')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class SonusAIError(Exception):
    def __init__(self, value):
        logger.error(value)


# create file handler
def create_file_handler(filename: str):
    fh = logging.FileHandler(filename=filename, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# update console handler
def update_console_handler(verbose: bool):
    if not verbose:
        logger.removeHandler(console_handler)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)


# write initial log message
def initial_log_messages(name: str):
    from datetime import datetime
    from getpass import getuser
    from os import getcwd
    from socket import gethostname
    from sys import argv

    logger.info(f'SonusAI {__version__}')
    logger.info(f'{name}')
    logger.info('')
    logger.debug(f'Host:      {gethostname()}')
    logger.debug(f'User:      {getuser()}')
    logger.debug(f'Directory: {getcwd()}')
    logger.debug(f'Date:      {datetime.now()}')
    logger.debug(f'Command:   {" ".join(argv)}')
    logger.debug('')
