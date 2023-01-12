from .Response import Response


def response_optimized(func):
    def inner(*args, **kwargs):
        reqs = Response(func(*args, **kwargs))  # Response对象
        return reqs

    return inner


