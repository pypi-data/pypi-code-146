'''
Logger confiiguration:
Copyright 2022 Reyes Ruiz
https://github.com/Los-Vaqueros-Western-Wear/Scripts
'''

import logging

def set_logger(module_name, loglevel='INFO'):
    '''
    logger
    '''
    logger = logging.getLogger(module_name)
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logger.setLevel(numeric_level)
    if not logger.handlers:
        channel = logging.StreamHandler()
        channel.setLevel(numeric_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        channel.setFormatter(formatter)
        logger.addHandler(channel)
    return logger
