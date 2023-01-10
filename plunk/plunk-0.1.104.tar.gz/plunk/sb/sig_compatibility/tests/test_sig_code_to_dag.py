import pytest
from plunk.sb.sig_compatibility.sig_code_to_dag import is_compatible
from i2 import Sig


def test_dummy():
    return True


def f(w, ww, www):
    return w * ww + www


def f_new(www, /, ww=2, *, w: int = 1):
    return w * ww + www


def test_comp_sig():
    assert is_compatible(f, Sig(f_new))
