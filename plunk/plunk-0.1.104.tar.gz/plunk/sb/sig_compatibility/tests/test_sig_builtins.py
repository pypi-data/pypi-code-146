import pytest
from plunk.sb.sig_compatibility.sig_builtins import (
    args_for_builtin,
    args_str_from_sig,
    sig_to_lambda,
    builtin_func_from_name,
)
from i2 import Sig
from i2.tests.util import sig_to_inputs, function_is_compatible_with_signature
from i2.tests.util import sig_to_inputs, _sig_to_inputs, sig_to_func


from typing import Iterable, Iterator, Callable, Any
from i2.signatures import dict_of_attribute_signatures
from i2.tests.util import call_raises_signature_error


@dict_of_attribute_signatures
class names:
    def bool(x: Any, /) -> bool:
        ...

    # def breakpoint(*args, **kwargs):
    #    ...

    def bytearray(iterable_of_ints: Iterable[int]):  # no sig possible without wrapping
        ...

    def bytes(
        string: str, encoding=None, errors=None
    ):  # no sig possible without wrapping
        ...

    def classmethod(function: Callable, /):
        ...

    def dict(**kwargs):
        ...

    def frozenset(
        iterable: Iterable = None,
    ):  # no sig possible without wrapping: zero or one argument
        ...

    def int(x, base=10, /):  #
        ...

    def iter(callable: Callable, sentinel=None, /):  # TODO check
        ...

    def max(*args, **keywords):
        ...

    def min(*args, **keywords):
        ...

    def next(iterator: Iterator, default=None):  # No Sig possible without wrapping
        ...

    def range(stop):  # No sig possible without wrapping
        ...  # TODO treat range(start, stop)

    def set(iterable: Iterable = None):  # No sig possible without wrapping
        ...

    def slice(start=None, stop=None, step=None):  # No sig possible without wrapping
        ...  # TODO incorrect !!

    def staticmethod(function: Callable, /):
        ...

    def str(bytes_or_buffer, encoding=None, errors=None, /):
        ...

    def super(type_, obj=None, /):
        ...

    def type(name, bases=None, dict=None, /):
        ...

    def vars(*obj):
        ...

    def zip(*iterables: Iterable):
        ...


def is_valid_call(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except BaseException:
        return False
    return True


foo_bool = None


def test_bool():
    name = 'bool'
    names_dict = names

    sig = Sig(names_dict[name])
    f = sig_to_func(sig)

    # args = args_str_from_sig(sig)
    # exec(f"global foo_bool\ndef foo_bool({args}):\n  return None")
    # f = foo_bool
    assert not call_raises_signature_error(f, '12')
    # assert not call_raises_signature_error(f, "12")
    assert not call_raises_signature_error(f, 5)
    assert function_is_compatible_with_signature(bool, sig)


# def test_breakpoint():
#     name = "breakpoint"
#     names_dict = names

#     sig = Sig(names_dict[name])
#     f = sig_to_func(sig)

#     assert not call_raises_signature_error(f, "12")
#     assert not call_raises_signature_error(f, 5)
#     assert function_is_compatible_with_signature(breakpoint, sig)


def test_bytearray():
    name = 'bytearray'
    names_dict = names
    sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_bytearray\ndef foo_bytearray({args}):\n  return None")
    # f = foo_bytearray
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, [1, 2, 4])
    # assert not call_raises_signature_error(f, 5)


def test_bytes():
    name = 'bytes'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_bytes\ndef foo_bytes({args}):\n  return None")
    # f = foo_bytes
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, [1, 2, 4])


def test_classmethod():
    name = 'classmethod'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_classmethod\ndef foo_classmethod({args}):\n  return None")
    # f = foo_classmethod

    # class X(object):
    #         def f(*args, **kwds): return args, kwds
    #         f = classmethod(f)
    # class Y(X):
    #     pass
    # assert X.f() == ((X,), {})
    # assert X.f(42, x=43) == ((X, 42), {'x': 43})
    # assert X().f() == ((X,), {})
    # assert X().f(42, x=43) == ((X, 42), {'x': 43})
    # assert Y.f() == ((Y,), {})
    # assert Y.f(42, x=43) == ((Y, 42), {'x': 43})
    # assert Y().f() == ((Y,), {})
    # assert Y().f(42, x=43) == ((Y, 42), {'x': 43})

    sig = Sig(names_dict[name])
    f = sig_to_func(sig)

    def g(*args, **kwargs):
        return args, kwargs

    assert not call_raises_signature_error(f, g)
    assert function_is_compatible_with_signature(classmethod, sig)


def test_dict():
    name = 'dict'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_dict\ndef foo_dict({args}):\n  return None")
    # f = foo_dict
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, {'a': 12, 'b': 5})
    assert not call_raises_signature_error(f, 3)
    assert function_is_compatible_with_signature(dict, sig)


def test_frozenset():
    name = 'frozenset'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_frozenset\ndef foo_frozenset({args}):\n  return None")
    # f = foo_frozenset
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, None)
    assert not call_raises_signature_error(f, [1, 2, 3])


def test_int():
    name = 'int'
    # f = builtin_func_from_name(name)
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_int\ndef foo_int({args}):\n  return None")
    # f = foo_int
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    # assert not call_raises_signature_error(f, "12")
    # assert not call_raises_signature_error(f, [12])

    # assert not call_raises_signature_error(f, "01001", base=2)
    assert function_is_compatible_with_signature(int, sig)


def test_iter():
    name = 'iter'
    names_dict = names
    # sig = Sig(names_dict[name])
    # print(sig)
    # args = args_str_from_sig(sig)
    # exec(f"global foo_iter\ndef foo_iter({args}):\n  return None")
    # f = foo_iter
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    # assert not call_raises_signature_error(f, [1, 2, 3, 4])
    # assert not call_raises_signature_error(f, 12)
    # assert not call_raises_signature_error(f, 12, "sentinel")
    # # assert not call_raises_signature_error(f, 12, sentinel=14)
    # pytest.raises(TypeError, f)
    assert function_is_compatible_with_signature(iter, sig)

    # print(f(42, 42))
    # pytest.raises(TypeError, f, 42, 42)


def test_max():
    name = 'max'
    names_dict = names
    # f = builtin_func_from_name(name)
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_{name}")

    # exec(f"global foo_max\ndef foo_max({args}):\n  return None")
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, [1, 2, 3, 4])
    assert not call_raises_signature_error(f, 'fake')
    assert function_is_compatible_with_signature(max, sig)


def test_min():
    name = 'min'
    names_dict = names
    # f = builtin_func_from_name(name)
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # # exec(f"global foo_{name}")
    # exec(f"global foo_min\ndef foo_min({args}):\n  return None")
    # f = foo_min
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, [1, 2, 3, 4])
    assert not call_raises_signature_error(f, 'fake')
    assert function_is_compatible_with_signature(min, sig)


def test_next():
    name = 'next'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_next\ndef foo_next({args}):\n  return None")
    # f = foo_next
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, [1, 2, 3, 4])


def test_range():
    name = 'range'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_range\ndef foo_range({args}):\n  return None")
    # f = foo_range
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, 3)


def test_set():
    name = 'set'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_set\ndef foo_set({args}):\n  return None")
    # f = foo_set
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, [1, 2, 3, 4])


def test_slice():
    name = 'slice'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_slice\ndef foo_slice({args}):\n  return None")
    # f = foo_slice
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, 2, 4)


def test_staticmethod():
    name = 'staticmethod'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_staticmethod\ndef foo_staticmethod({args}):\n  return None")
    # f = foo_staticmethod
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)

    def g(*args, **kwargs):
        return args, kwargs

    assert not call_raises_signature_error(f, g)
    assert function_is_compatible_with_signature(staticmethod, sig)


def test_str():
    name = 'str'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_str\ndef foo_str({args}):\n  return None")
    # f = foo_str
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, 12)
    assert function_is_compatible_with_signature(str, sig)


def test_super():
    name = 'super'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_super\ndef foo_super({args}):\n  return None")
    # f = foo_super
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    # assert not call_raises_signature_error(f, "a_type")
    # assert not call_raises_signature_error(f, "a_type", obj="an_obj")
    assert function_is_compatible_with_signature(super, sig)


def test_type():
    name = 'type'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_type\ndef foo_type({args}):\n  return None")
    # f = foo_type
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    # assert not call_raises_signature_error(f, "a_name")
    # assert not call_raises_signature_error(f, name="a_name")

    # assert not call_raises_signature_error(
    #     f, name="a_type", bases="an_obj", dict="a_dict"
    # )
    assert function_is_compatible_with_signature(type, sig)


def test_vars():
    name = 'vars'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_vars\ndef foo_vars({args}):\n  return None")
    # f = foo_vars
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, ['obj_1', 'obj_2'])
    assert function_is_compatible_with_signature(vars, sig)


def test_zip():
    name = 'zip'
    names_dict = names
    # sig = Sig(names_dict[name])

    # args = args_str_from_sig(sig)
    # exec(f"global foo_zip\ndef foo_zip({args}):\n  return None")
    # f = foo_zip
    sig = Sig(names_dict[name])
    f = sig_to_func(sig)
    assert not call_raises_signature_error(f, ['obj_1', 'obj_2'])
    assert function_is_compatible_with_signature(zip, sig)


def test_call_raises():
    assert call_raises_signature_error(lambda x, /, y: None, x=1, y=2)


if __name__ == '__main__':
    test_bool()
    # test_breakpoint() # calls the debugger
    test_bytearray()
    # test_bytes()
    test_classmethod()
    # test_dict()  # check
    test_int()  # check
    # test_frozenset()
    # test_max() #check
    # test_min() # check
    test_next()
    test_iter()
    # test_set()
    # test_slice()
    test_staticmethod()
    test_str()  # check
    test_super()
    test_type()
    # test_vars()
    # test_zip()
