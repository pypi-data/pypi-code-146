"""Utils"""
from typing import Optional
import os
import datetime
import logging


def get_file_location(location: Optional[str] = None):
    """return file location"""
    if location is None:
        location = os.environ.get('DATAGENIE_DIR')
    if location is None:
        location = '.'
    location = os.path.abspath(location)
    if not os.path.exists(location):
        logger(f'{location} does not exists', error=True)
        return None
    if not os.path.isdir(location):
        logger(f'{location} is not a directory', error=True)
        return None
    return location


def generate_file_name(file_type: str, file_name: Optional[str] = None,
                       date_formatter: str = '%Y-%m-%d-%H-%M-%S'):
    """generates file name for datasets"""
    if file_name:
        # Strip file extension from file_name if it is already included
        file_name = file_name.rsplit('.', 1)[0]
    else:
        now = datetime.datetime.now()
        formatted_date = now.strftime(date_formatter)
        file_name = f'datagenie_{formatted_date}'
    return f'{file_name}.{file_type}'


def get_datagenie_env():
    """returns all the env variables related to datagenie"""
    env = {}
    for key, value in os.environ.items():
        if key.startswith('DATAGENIE_'):
            env[key] = value
    return env


def logger(value, *, debug=True, info=False, error=False):
    """ logger for datagenie"""
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    if info:
        logging.getLogger().setLevel(logging.INFO)
        logging.info('%s', value)
    if error:
        logging.getLogger().setLevel(logging.ERROR)
        logging.error('%s', value)
