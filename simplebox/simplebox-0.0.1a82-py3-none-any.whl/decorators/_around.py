#!/usr/bin/env python
# -*- coding:utf-8 -*-
from functools import wraps
from typing import List, Callable, Tuple, Dict

from ._around_impl import around_impl


def around(before: List[Callable] or Callable = None, after: List[Callable] or Callable = None,
           catch: bool = False):
    """
    Preform facet operations on functions
    It supports injecting the return value of the preceding hook function into the decorated function
    Support to inject the return value of the decorated function into the post hook function.

    The decorated function can get the return value of the fore hook function through the "func_return" parameter,
    and the after hook function can get the return value of the decorated function via the "func_return" parameter.

    all callback functions can and only support communication via the chain keyword parameter. example: callback() is ok,
    callback(chain=None) is ok, callback(chain=None, other=None) is ok(other arg will not be assigned), callback(other, chain=None) will happend exception


    For example:
        from simplebox.decorators import around


        def setup_module(chain):
            chain["x"] += 1


        def teardown_module(chain=None):
            chain["x"] += 1


        class Hook(object):

            @staticmethod
            def setup_static(chain=None):
                chain["x"] += 1

            @classmethod
            def setup_class(cls, chain=None):
                chain["x"] += 1

            def setup_instance(self, chain=None):
                chain["x"] += 1

            @staticmethod
            def teardown_static(chain=None):
                chain["x"] += 1

            @classmethod
            def teardown_class(cls, chain=None):
                chain["x"] += 1

            def teardown_instance(self, chain=None):
                chain["x"] += 1


        hook = Hook()


        class AroundTest(object):

            @staticmethod
            def setup_static(chain=None):
                chain["x"] += 1

            @classmethod
            def setup_class(cls, chain=None):
                chain["x"] += 1

            def setup_instance(self, chain=None):
                chain["x"] += 1

            @staticmethod
            def teardown_static(chain=None):
                chain["x"] += 1

            @classmethod
            def teardown_class(cls, chain=None):
                chain["x"] += 1

            def teardown_instance(self, chain=None):
                chain["x"] += 1

            @around(before=[setup_module, hook.setup_static, hook.setup_class, hook.setup_instance, setup_static, setup_class,
                            setup_instance],
                    after=[teardown_instance, teardown_class, teardown_static, hook.teardown_instance, hook.teardown_class,
                           hook.teardown_static, teardown_module])
            def case1(self, a, b, *args, e, j=None, chain=None, **kwargs):
                chain["x"] += 1
                return "instance.case1"

            @staticmethod
            @around(before=[setup_module, hook.setup_static, hook.setup_class, hook.setup_instance, setup_static],
                    after=[teardown_static, hook.teardown_instance, hook.teardown_class,hook.teardown_static, teardown_module])
            def case2(a, b, *args, e, j=None, chain=None, **kwargs):
                chain["x"] += 1
                return "static.case2"

            @classmethod
            @around(before=[setup_module, hook.setup_static, hook.setup_class, hook.setup_instance, setup_static, setup_class],
                    after=[teardown_class, teardown_static, hook.teardown_instance, hook.teardown_class,hook.teardown_static, teardown_module])
            def case3(cls, a, b, *args, e, j=None, chain=None, **kwargs):
                chain["x"] += 1
                return "class.case3"


        @around(before=[setup_module, hook.setup_static, hook.setup_class, hook.setup_instance])
        def case1(a, b, *args, e, j=None, chain=None, **kwargs):
            chain["x"] += 1
            return "case1"


        if __name__ == '__main__':
            chain = {"x": 1}
            result = AroundTest().case1(1, 2, 3, 4, e=5, j=6, h=7, chain=chain)
            assert chain["x"] == 16
            assert result == "instance.case1", result

            chain = {"x": 1}
            result = AroundTest().case2(1, 2, 3, 4, e=5, j=6, h=7, chain=chain)
            assert chain["x"] == 12, chain
            assert result == "static.case2", result

            chain = {"x": 1}
            result = AroundTest().case3(1, 2, 3, 4, e=5, j=6, h=7, chain=chain)
            assert chain["x"] == 14
            assert result == "class.case3", result

            chain = {"x": 1}
            result = AroundTest.case2(1, 2, 3, 4, e=5, j=6, h=7, chain=chain)
            assert chain["x"] == 12
            assert result == "static.case2", result

            chain = {"x": 1}
            result = AroundTest.case3(1, 2, 3, 4, e=5, j=6, h=7, chain=chain)
            assert chain["x"] == 14
            assert result == "class.case3", result

            chain = {"x": 1}
            result = case1(1, 2, 3, 4, e=5, j=6, h=7, chain=chain)
            assert chain["x"] == 6
            assert result == "case1", result


    :param catch: decorated function throw exception when runtime, if True, will catch exception and run hook function,
                    then throw origin exception. If False, throw the exception directly.
                    Valid only for after hook functions.
    :param before:
        Preceding hook function before the decorated function is executed.
        If "before" is a dictionary, the key is the hook function object,
        and the value is the parameter of the hook function.
        When the hook function is executed, it will be passed to the hook function in the form of key value pairs.
        If "before" is a list, it means that the hook function has no parameters.
        If "before" is an executable object, the hook function is directly executed
    :param after:
        Post hook function.
        reference resources @params before
    """

    def _inner(func):
        @wraps(func)
        def _wrapper(*args: Tuple, **kwargs: Dict):
            result = around_impl(func, before, after, catch, *args, **kwargs)
            return result
        return _wrapper
    return _inner


__all__ = [around]
