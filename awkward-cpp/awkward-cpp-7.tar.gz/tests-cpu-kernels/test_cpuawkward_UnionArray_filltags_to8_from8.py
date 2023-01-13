# AUTO GENERATED ON 2023-01-12 AT 23:40:21
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import ctypes
import pytest

from awkward_cpp.cpu_kernels import lib

def test_cpuawkward_UnionArray_filltags_to8_from8_1():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    totagsoffset = 3
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = [123, 123, 123, 3.0, 3.0, 3.0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_cpuawkward_UnionArray_filltags_to8_from8_2():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    totagsoffset = 3
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = [123, 123, 123, 4.0, 4.0, 4.0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_cpuawkward_UnionArray_filltags_to8_from8_3():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    totagsoffset = 3
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = [123, 123, 123, 4.0, 4.0, 4.0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_cpuawkward_UnionArray_filltags_to8_from8_4():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    totagsoffset = 3
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = [123, 123, 123, 3.0, 3.0, 3.0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

def test_cpuawkward_UnionArray_filltags_to8_from8_5():
    totags = [123, 123, 123, 123, 123, 123]
    totags = (ctypes.c_int8*len(totags))(*totags)
    totagsoffset = 3
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    base = 3
    funcC = getattr(lib, 'awkward_UnionArray_filltags_to8_from8')
    ret_pass = funcC(totags, totagsoffset, fromtags, length, base)
    pytest_totags = [123, 123, 123, 3.0, 3.0, 3.0]
    assert totags[:len(pytest_totags)] == pytest.approx(pytest_totags)
    assert not ret_pass.str

