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

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_1():
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_2():
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_3():
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_4():
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_5():
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    ret_pass = funcC(fromoffsets, offsetslength, size)
    assert not ret_pass.str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_6():
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_7():
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_8():
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_9():
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_10():
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_11():
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_12():
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_13():
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_14():
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_15():
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_16():
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_17():
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_18():
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_19():
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_20():
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_21():
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 3
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_22():
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_23():
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 1
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_24():
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 2
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    assert funcC(fromoffsets, offsetslength, size).str

def test_cpuawkward_RegularArray_broadcast_tooffsets_64_25():
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    fromoffsets = (ctypes.c_int64*len(fromoffsets))(*fromoffsets)
    offsetslength = 3
    size = 0
    funcC = getattr(lib, 'awkward_RegularArray_broadcast_tooffsets_64')
    ret_pass = funcC(fromoffsets, offsetslength, size)
    assert not ret_pass.str

