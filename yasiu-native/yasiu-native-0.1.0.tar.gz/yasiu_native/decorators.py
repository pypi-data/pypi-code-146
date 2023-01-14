def flexible_decorator(decor_func):
    """
    Decorator that asserts function is called even without ().
    Child decorator receives function and decoration variables if any were used.
    Supports both positional and key arguments.


    Args:
        **decor_func:

    Returns:

    Example:
          @flexible_decorator
          def custom_decorator(func, decorative_argument):

            def inner(*args, **kwargs):
                "Use decorative arguments to modify decorator"
                ret = func(*args, **kwargs)
                return ret

            return inner


    """

    def wrapper(*args, **kw):
        if len(args) > 0:
            fun1 = args[0]

        else:
            fun1 = None

        if callable(fun1):
            "Passed callable as first argument, without calling () in decoration"
            return decor_func(fun1)

        def inner(fun2, ):
            ret = decor_func(fun2, *args, **kw)  # (*a2, **kw2)

            return ret

        return inner

    return wrapper


def flexible_decorator_2d(decor_func):
    """
    Decorator that asserts function is called even without ().
    Child decorator receives function and decoration variables if any were used.
    Supports both positional and key arguments.


    Args:
        **decor_func:

    Returns:

    Example:

          @flexible_decorator_2d
          def custom_decorator(decorative_argument):

            def wrapper(func):

                def inner(*args, **kwargs):
                    "Use decorative arguments to modify decorator"
                    ret = func(*args, **kwargs)
                    return ret

                return inner

            return wrapper

    """

    def wrapper(*args, **kw):
        if len(args) > 0:
            fun1 = args[0]

        else:
            fun1 = None

        if callable(fun1):
            "Passed callable as first argument, without calling () in decoration"
            return decor_func()(fun1)

        def inner(fun2, ):
            ret = decor_func(*args, **kw)(fun2)

            return ret

        return inner

    return wrapper


__all__ = ['flexible_decorator', 'flexible_decorator_2d']
