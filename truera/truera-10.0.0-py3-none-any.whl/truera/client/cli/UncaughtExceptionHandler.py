"""
Command-line tools exception handler for unchaught exceptions. Only prints out
the exceptions using click.
"""

import functools
import sys
from typing import Type

import click

from truera.client.errors import SimpleException


class UncaughtExceptionHandler():
    """
    Handle uncaught exceptions by printing them using click.echo . You can use
    this class as a context manager like:

        ```
        with UncaughtExceptionHandler():
            # do something that can throw
        ```

    Or by using the wrap method like:

        ```
        wrap(somemethodthatcanfail, arg1, arg2, ...)
        ```

    where the args are sent to `somemethodthatcanfail`. Or by decorating a method like:

        ```
        @UncaughtExceptionHandler.decorate
        def somemethodthatcanfail(...): ...
        ```
    """

    # context manager requirement
    def __init__(self):
        pass

    # context manager requirement
    def __enter__(self):
        pass

    # context manager requirement
    def __exit__(
        self, exc_type: Type[BaseException], exc_val: BaseException, traceback
    ):
        if exc_type is not None:
            if isinstance(exc_val, SimpleException):
                click.echo(exc_val.message)
            else:
                click.echo(exc_val)
                raise exc_val

            sys.exit(1)

    @staticmethod
    def decorate(f):
        # https://click.palletsprojects.com/en/7.x/commands/#decorating-commands

        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            with UncaughtExceptionHandler():
                return ctx.invoke(f, *args, **kwargs)

        return functools.update_wrapper(wrapper, f)

    @staticmethod
    def wrap(f, *args, **kwargs):
        with UncaughtExceptionHandler():
            return f(*args, **kwargs)
