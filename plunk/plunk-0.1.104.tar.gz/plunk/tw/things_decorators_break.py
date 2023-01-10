# ---------------------------------------------------------------------------------------
# The following is to demo that (in a notebook at least) when we import this module,
# the decorated functions don't appear in tab-completion list, though they ARe
# attributes of the module object.


# This one is tab-complete visible
def bar(x):
    return x


# 1 ----------
def my_deco(func):
    print(f'{func.__name__} is being called')

    def wrapped_func(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapped_func


# Not even importable!!!
@my_deco
def foo_my_deco(x):
    return x


# 2 ----------
from functools import wraps


def foo(x):  # this will be overwritten by foo_wraps which will be given the foo name
    return x


# Not tab-complete visible
@wraps(foo)
def foo_wraps(x):
    return x


# 3 ----------
from i2.wrapper import wrap


# Not tab-complete visible
@wrap
def foo_wrap(x):
    return x


# 4 ----------
from i2.deco import double_up_as_factory


# Not tab-complete visible
@double_up_as_factory
def foo_double_up_as_factory(x=None):
    return x


# test code (to be run in notebook
def test_decorated_funcs():
    """Meant to be copied"""
    # this shows that they exist (but)

    import plunk.tw.things_decorators_break as m

    expected_func_names = (
        'foo_my_deco',
        'foo_wraps',
        'foo_wrap',
        'foo_double_up_as_factory',
    )
    assert all(x in dir(m) for x in expected_func_names)
    dir(m)

    # and we can import them with from... import... idiom:
    from plunk.tw.things_decorators_break import (
        foo_my_deco,
        foo_wraps,
        foo_wrap,
        foo_double_up_as_factory,
    )

    # But in jupyter notebook, can't tab-complete with that idiom (but can tab
    # complete bar)
