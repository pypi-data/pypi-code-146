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

def test_cpuawkward_RegularArray_rpad_and_clip_axis1_64_1():
    toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123]
    toindex = (ctypes.c_int64*len(toindex))(*toindex)
    target = 3
    size = 3
    length = 3
    funcC = getattr(lib, 'awkward_RegularArray_rpad_and_clip_axis1_64')
    ret_pass = funcC(toindex, target, size, length)
    pytest_toindex = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)
    assert not ret_pass.str

