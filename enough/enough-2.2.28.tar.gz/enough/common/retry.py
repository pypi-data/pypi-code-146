import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)


class RetryException(Exception):
    pass


def retry(exceptions, tries=2, delay=1, exponential=True):
    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries + 1, delay
            while mtries > 0:
                try:
                    return f(*args, **kwargs)
                except exceptions as e:
                    logger.info('%s: %s, Retrying in %s seconds...', f.__qualname__, e, mdelay)
                    if mtries == tries + 1:
                        logger.debug("", exc_info=True)
                    time.sleep(mdelay)
                    mtries -= 1
                    if exponential:
                        mdelay *= 2
            raise RetryException("Number of retries exceeded for function " + f.__name__)
        return f_retry
    return deco_retry
