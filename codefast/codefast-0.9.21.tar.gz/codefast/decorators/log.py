#!/usr/bin/env python
from codefast.logger import app_log as logger

def time_it(func):
    def wrapper(*args, **kwargs):
        import time
        start = time.time()
        logger.info('Calling function: {}'.format(func.__name__))
        res = func(*args, **kwargs)
        end = time.time()
        logger.info('Function {} took {:<.4} seconds'.format(
            func.__name__, end - start))
        return res

    return wrapper
