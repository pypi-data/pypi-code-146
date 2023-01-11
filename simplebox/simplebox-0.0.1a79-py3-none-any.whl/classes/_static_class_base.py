#!/usr/bin/env python
# -*- coding:utf-8 -*-

from ..exceptions import raise_exception, InstanceException


class StaticClass(type):
    """
    Create a class that cannot be instantiated
    Example:
        Class Foo(metaclass=StaticClass):
            pass
        Foo() # raise exception
    """
    def __call__(cls, *args, **kwargs):
        raise_exception(InstanceException(f"Class '{cls.__name__}' cannot be instantiated!!!"))


__all__ = [StaticClass]
