from functools import wraps
from inspect import signature

from elasticapm import capture_span

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
            logger.info('[%s] %s(%s)' % (
                "kili_common_storage", func.__name__, arguments_str))

            with capture_span(func.__name__):
                result = func(*args, **kwargs)
                if ignore_res is False:
                    logger.info('[%s] %s_result=%r' % (
                        "kili_common_storage", func.__name__, result))

            return result
        return wrapper
    return func_wrapper
