# -*- coding: utf-8 -*-

import time
from django.core.cache import caches
import logging
import hashlib

logger = logging.getLogger(__name__)


def timeit(f):

    def timed(*args, **kw):
        # import pdb; pdb.set_trace()
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        # logger.info('func:%r args:[%r, %r] took: %2.4f sec' % (f.__name__, args, kw, te - ts))
        logger.info('==================func:%r  took: %2.4f sec' % (f.__name__, te - ts))
        return result
    return timed


def cache_func_result_decorator(ex=300):
    '''
    缓存某个方法的运行结果
    :params ex: 过期时间, 单位 s   默认 300
    '''
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            cache_handler = caches.get('default')
            if not cache_handler:
                return func(*args, **kwargs)

            cache_key_info = str(func.__name__) + str(args) + str(kwargs)
            cache_key = hashlib.md5().update(cache_key_info).hexdigest()
            cached_data = cache_handler.get(cache_key)
            if cached_data:
                return cached_data['data']
            else:
                data = func(*args, **kwargs)
                cache_handler.set(cache_key, {'data': data}, ex)
                return data
        return _wrapper
    return _decorator
