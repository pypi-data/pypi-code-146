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

def test_cpuawkward_UnionArray8_U32_regular_index_1():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    current = [123, 123, 123]
    current = (ctypes.c_uint32*len(current))(*current)
    size = 3
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray8_U32_regular_index')
    ret_pass = funcC(toindex, current, size, fromtags, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_current = [3, 0, 0]
    assert current[:len(pytest_current)] == pytest.approx(pytest_current)
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_U32_regular_index_2():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    current = [123, 123, 123]
    current = (ctypes.c_uint32*len(current))(*current)
    size = 3
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray8_U32_regular_index')
    ret_pass = funcC(toindex, current, size, fromtags, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_current = [0, 3, 0]
    assert current[:len(pytest_current)] == pytest.approx(pytest_current)
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_U32_regular_index_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    current = [123, 123, 123]
    current = (ctypes.c_uint32*len(current))(*current)
    size = 3
    fromtags = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray8_U32_regular_index')
    ret_pass = funcC(toindex, current, size, fromtags, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_current = [0, 3, 0]
    assert current[:len(pytest_current)] == pytest.approx(pytest_current)
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_U32_regular_index_4():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    current = [123, 123, 123]
    current = (ctypes.c_uint32*len(current))(*current)
    size = 3
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray8_U32_regular_index')
    ret_pass = funcC(toindex, current, size, fromtags, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_current = [3, 0, 0]
    assert current[:len(pytest_current)] == pytest.approx(pytest_current)
    assert not ret_pass.str

def test_cpuawkward_UnionArray8_U32_regular_index_5():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_uint32*len(toindex))(*toindex)
    current = [123, 123, 123]
    current = (ctypes.c_uint32*len(current))(*current)
    size = 3
    fromtags = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    fromtags = (ctypes.c_int8*len(fromtags))(*fromtags)
    length = 3
    funcC = getattr(lib, 'awkward_UnionArray8_U32_regular_index')
    ret_pass = funcC(toindex, current, size, fromtags, length)
    pytest_toindex = [0, 1, 2]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    pytest_current = [3, 0, 0]
    assert current[:len(pytest_current)] == pytest.approx(pytest_current)
    assert not ret_pass.str

