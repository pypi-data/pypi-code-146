import pytest
from pytest import fixture
from i2 import Sig

from plunk.sb.sig_compatibility.sig_comp import (
    transform_key,
    variadic_compatibility,
    variadics_from_sig,
)


def test_transform_key():
    d = {'key1': 12, 'key2': 23}
    func = lambda x: x.upper()
    result = transform_key(d, func)
    expected = {'KEY1': 12, 'KEY2': 23}
    assert result == expected


def test_variadics_from_sig():
    def f1(a, b, /, c, *args, k1=12):
        pass

    def f2(a, b, /, c, *args, k1=12, **kwargs):
        pass

    sig1 = Sig(f1)
    sig2 = Sig(f2)
    assert variadics_from_sig(sig1) == (True, False)
    assert variadics_from_sig(sig2) == (True, True)


def test_variadic_compatibility():
    vpk = True, False, True, True
    assert not variadic_compatibility(*vpk)
    vpk = True, True, True, True
    assert variadic_compatibility(*vpk) is None
    vpk = True, True, True, False
    assert not variadic_compatibility(*vpk)
