from functools import wraps

cache = {}
func_caches = {}


def cached(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        module = getattr(func, "__module__", "")
        name = getattr(func, "__name__", "")
        key = module + name
        if key in func_caches and func_caches[key] is not None:
            return func_caches[key]

        func_caches[key] = func(*args, **kwargs)
        return func_caches[key]

    return wrapper
