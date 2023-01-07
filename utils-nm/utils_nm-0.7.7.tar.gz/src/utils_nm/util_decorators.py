# util_decorators.py
# -*- coding: utf-8 -*-

"""
Decorators which serve for general purposes
"""

import functools


# ______________________________________________________________________________________________________________________


def timed(reps: int = 1):
    """
    decorator factory function which creates a decorator to measure execution time of functions

    Args:
        reps: how many times to repeat executing the function

    Returns:
        a decorator function
    """

    def dec(fn):
        """
        decorator

        Args:
            fn: the function to be decorated

        Returns:
            decorated function
        """

        from time import perf_counter

        @functools.wraps(fn)
        def inner(*args, **kwargs):
            """
            closure which runs the decorator code and executes the function

            Args:
                args: arbitrary number of positional arguments
                kwargs: arbitrary number of keyword only arguments

            Returns:
                the result of the function call to fn
            """

            fn_result = None
            arguments = ', '.join([str(a) for a in args])
            kw_arguments = ', '.join([f'{k}={v}' for k, v in kwargs.items()])
            all_arguments = ', '.join(filter(None, [arguments, kw_arguments]))

            total_elapsed = 0

            for i in range(reps):
                start = perf_counter()
                fn_result = fn(*args, **kwargs)
                total_elapsed += (perf_counter() - start)
            avg_elapsed = total_elapsed / reps

            if reps == 1:
                print(f'{fn.__name__}({all_arguments}) execution time : {avg_elapsed}')
            else:
                print(f'{fn.__name__}({all_arguments}) avg execution time after {reps} reps: {avg_elapsed}')
            return fn_result

        return inner

    return dec


# ______________________________________________________________________________________________________________________
