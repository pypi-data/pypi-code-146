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

def test_cpuawkward_ListArray64_localindex_64_1():
    toindex = [123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    offsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [123, 123, 0, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_cpuawkward_ListArray64_localindex_64_2():
    toindex = [123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    offsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

def test_cpuawkward_ListArray64_localindex_64_3():
    toindex = [123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    offsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    offsets = (ctypes.c_int64*len(offsets))(*offsets)
    length = 3
    funcC = getattr(lib, 'awkward_ListArray64_localindex_64')
    ret_pass = funcC(toindex, offsets, length)
    pytest_toindex = [0, 1, 0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

