from functools import wraps


def decorator_with_kwargs(orig_decorator: callable):
    """
    Super-decorator to create decorator that can handle kwargs

    IMPORTANT: First argument of your decorator hould always catch decorating function
               and have default value None. It's allso aloow you to run your decoator
               without kwargs as a regular one, so that's why all other kwargs shoud
               have implemented default value

    Example:
    >>> import dryco as dc
    >>>
    >>>
    >>> @dc.decorator_with_kwargs
    >>> def add_greetings(original_func: callable = None, message=None):
    >>>     'Print greeting message before function ran'
    >>>
    >>>     def func_with_greetings(*args, **kwargs):
    >>>         if message is None:  # print "Hello, world!" if message isn't set
    >>>             print("Hello, world!")
    >>>         else:
    >>>             print(message)
    >>>         original_func(*args, **kwargs)  # call original function
    >>>
    >>>     return func_with_greetings
    >>>
    >>>
    >>> @add_greetings
    >>> def calculations_1():
    >>>     print('1 + 1 =', 1 + 1)
    >>>
    >>>
    >>> @add_greetings(message='Wow, math is cool!')
    >>> def calculations_2():
    >>>     print('2 + 2 =', 2 + 2)
    >>>
    >>>
    >>> calculations_1()
    >>> # Hello, world!
    >>> # 1 + 1 = 2
    >>> calculations_2()
    >>> # Wow, math is cool!
    >>> # 2 + 2 = 4

    :param orig_decorator: Original decorator
    :return: Decorator that can handle kwargs
    """

    @wraps(orig_decorator)
    def patched_decorator(func: callable = None, *args, **kwargs):
        @wraps(func)
        def patched_decorator_with_kwargs(orig_func: callable):
            return orig_decorator(orig_func, *args, **kwargs)

        # calling without kwargs
        if func:
            return patched_decorator_with_kwargs(func)

        # calling with kwargs
        return patched_decorator_with_kwargs

    return patched_decorator


@decorator_with_kwargs
def method_not_allowed(method: callable, exception: Exception = None):
    @wraps(method)
    def not_allowed_method(*args, **kwargs):
        if exception is None:
            raise Exception("Method not allowed")
        raise exception

    return not_allowed_method


__all__ = ["decorator_with_kwargs", "method_not_allowed"]
