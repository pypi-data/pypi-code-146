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

def test_cpuawkward_ListOffsetArrayU32_compact_offsets_64_1():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromoffsets, length)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArrayU32_compact_offsets_64_2():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromoffsets, length)
    pytest_tooffsets = [0, 1, 1, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArrayU32_compact_offsets_64_3():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromoffsets, length)
    pytest_tooffsets = [0, -1, -2, -1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArrayU32_compact_offsets_64_4():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromoffsets, length)
    pytest_tooffsets = [0, -1, 1, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

def test_cpuawkward_ListOffsetArrayU32_compact_offsets_64_5():
    tooffsets = [123, 123, 123, 123]
    tooffsets = (ctypes.c_int64*len(tooffsets))(*tooffsets)
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_uint32*len(fromoffsets))(*fromoffsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListOffsetArrayU32_compact_offsets_64')
    ret_pass = funcC(tooffsets, fromoffsets, length)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)
    assert not ret_pass.str

