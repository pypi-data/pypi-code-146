from datetime import datetime
from functools import wraps
from inspect import signature

from .loggings import logger


def args_log(ignore_res=True):
    def func_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sig = signature(func)
            bind = sig.bind(*args, **kwargs).arguments
            arguments_str_list = []
            for k, v in list(bind.items()):
                if k.startswith("binary"):
                    arguments_str_list.append(
                        "%s=<binary>" % k if k != "self" else "%s" % k)
                else:
                    arguments_str_list.append(
                        "%s=%s" % (k, v) if k != "self" else "%s" % k)
            arguments_str = ", ".join(arguments_str_list)
            now = datetime.utcnow()
            logger.info(
                '[%s][UTC %s] %s(%s)' %
                ("kili_object_storage", datetime.strftime(now, "%Y-%m-%d %H:%M:%S"),
                 func.__name__, arguments_str))

            result = func(*args, **kwargs)
            if ignore_res is False:
                logger.info('[UTC %s] %s_result=%r' % (
                    datetime.strftime(now, "%Y-%m-%d %H:%M:%S"), func.__name__,
                    result))

            return result
        return wrapper
    return func_wrapper
