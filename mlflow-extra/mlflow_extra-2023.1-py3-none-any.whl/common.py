#!/usr/bin/env python3
'''
Common functionality.
'''

import logging


LOGGER = logging.getLogger(__name__)
DEFAULT_DIRECTORY = 'mlruns'


def configure_logging(level=logging.INFO):
    '''
    Configure logging.

    Args:
        level:
            The logging level.
    '''
    logging.basicConfig(
        style='{',
        format='[{asctime}] {levelname} {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=level
    )
