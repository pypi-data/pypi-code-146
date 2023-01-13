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

def test_cpuawkward_ListArrayU32_getitem_jagged_expand_64_1():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [1, 1, 1]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [1, 1, 1]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_expand_64_2():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [2, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 3]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_expand_64_3():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [2, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [1, 1, 1]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_expand_64_4():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [1, 1, 1]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 0, 0]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

def test_cpuawkward_ListArrayU32_getitem_jagged_expand_64_5():
    multistarts = [123, 123, 123]
    multistarts = (ctypes.c_int64*len(multistarts))(*multistarts)
    multistops = [123, 123, 123]
    multistops = (ctypes.c_int64*len(multistops))(*multistops)
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    singleoffsets = (ctypes.c_int64*len(singleoffsets))(*singleoffsets)
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstarts = (ctypes.c_uint32*len(fromstarts))(*fromstarts)
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    fromstops = (ctypes.c_uint32*len(fromstops))(*fromstops)
    jaggedsize = 1
    length = 3
    funcC = getattr(lib, 'awkward_ListArrayU32_getitem_jagged_expand_64')
    ret_pass = funcC(multistarts, multistops, singleoffsets, tocarry, fromstarts, fromstops, jaggedsize, length)
    pytest_multistarts = [0, 0, 0]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 0, 0]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    assert not ret_pass.str

