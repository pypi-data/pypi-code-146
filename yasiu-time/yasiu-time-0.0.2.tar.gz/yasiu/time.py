import time

from functools import wraps


def measure_perf_time_decorator(fmt=">4.1f"):
    """
    Example:
        @measure_perf_time_decorator()
        def func():
            ...

        @measure_perf_time_decorator(">4.1f")
        def func():
            ...

    Args:
        fmt: string

    Returns:

    """

    def decorator(fun):
        @wraps(wrapped=fun)
        def wrapper(*a, **kw):
            # fmt = ">4.1f"
            time0 = time.perf_counter()
            res = fun(*a, **kw)
            t_end = time.perf_counter()
            dur = t_end - time0
            if dur < 1e-3:
                timeend = f"{dur * 1000000:{fmt}} us"
            elif dur < 1:
                timeend = f"{dur * 1000:{fmt}} ms"
            else:
                timeend = f"{dur:{fmt}} s"
            print(f"{fun.__name__} perf exec time: {timeend}: ")

            return res

        return wrapper

    return decorator


def measure_real_time_decorator(fmt=">4.1f"):
    """
    Example:
        @measure_real_time_decorator()
        def func():
            ...

        @measure_real_time_decorator(">4.1f")
        def func():
            ...

    Args:
        fmt: string

    Returns:

    """

    def decorator(fun):
        @wraps(wrapped=fun)
        def wrapper(*a, **kw):
            # fmt = ">4.1f"
            time0 = time.time()
            res = fun(*a, **kw)
            t_end = time.time()
            dur = t_end - time0
            if dur < 1e-3:
                timeend = f"{dur * 1000000:{fmt}} us"
            elif dur < 1:
                timeend = f"{dur * 1000:{fmt}} ms"
            else:
                timeend = f"{dur:{fmt}} s"
            print(f"{fun.__name__} real exec time: {timeend}: ")

            return res

        return wrapper

    return decorator


__all__ = ['measure_perf_time_decorator', 'measure_real_time_decorator']

if __name__ == "__main__":
    def fun(N=10000000):
        a = [0] * 10
        for x in range(N):
            a[x % 5] = x * 3.5


    fun1 = measure_real_time_decorator()(fun)
    fun2 = measure_perf_time_decorator()(fun)

    fun1()
    fun2()
