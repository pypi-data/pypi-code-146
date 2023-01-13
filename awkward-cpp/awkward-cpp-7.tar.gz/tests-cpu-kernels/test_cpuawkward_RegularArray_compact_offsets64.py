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

def test_cpuawkward_RegularArray_compact_offsets64_1():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    length = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_compact_offsets64')
    ret_pass = funcC(tooffsets, length, size)
    pytest_tooffsets = [0, 3, 6, 9]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_RegularArray_compact_offsets64_2():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    length = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_compact_offsets64')
    ret_pass = funcC(tooffsets, length, size)
    pytest_tooffsets = [0, 2, 4, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_RegularArray_compact_offsets64_3():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    length = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_compact_offsets64')
    ret_pass = funcC(tooffsets, length, size)
    pytest_tooffsets = [0, 1, 2, 3]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_RegularArray_compact_offsets64_4():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    length = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_compact_offsets64')
    ret_pass = funcC(tooffsets, length, size)
    pytest_tooffsets = [0, 2, 4, 6]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_RegularArray_compact_offsets64_5():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    length = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_compact_offsets64')
    ret_pass = funcC(tooffsets, length, size)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

