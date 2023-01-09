import logging

from requests.exceptions import RequestException
from .cache import cache
from .setting import setting
from .cache import NO_ARGUMENT

logger = logging.getLogger(__name__)


def request_error_logging(func):
    """ The errors raise by request will be handler in here

    IF RAISE_REQUEST_ERROR = True
    the exception will be raise to upper level
    otherwise
    it will return a None
    """

    def wrapper(*args, **kwargs):
        ret = None
        try:
            ret = func(*args, **kwargs)
        except RequestException as e:
            logger.error(e)
            raise e
        return ret

    return wrapper


def no_arg(args):
    if len(args) == 1:
        new_args = (NO_ARGUMENT,)
        return NO_ARGUMENT
    else:
        return args[1]


def cache_it(keyword):
    def decorator(func):
        def wrapper(*args):
            #todo : deal with default argument
            ret = None
            if setting.CACHE_ON:
                ret = cache.get_cache(keyword, no_arg(args))
            if not ret:
                ret = func(*args)
                if setting.CACHE_ON:
                    cache.set_cache(keyword, ret, no_arg(args))
            return ret

        return wrapper

    return decorator
