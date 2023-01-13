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

def test_cpuawkward_index_rpad_and_clip_axis1_64_1():
    tostarts = [123, 123, 123]
    tostarts = (ctypes.c_int64*len(tostarts))(*tostarts)
    tostops = [123, 123, 123]
    tostops = (ctypes.c_int64*len(tostops))(*tostops)
    target = 3
    length = 3
    funcC = getattr(lib, 'awkward_index_rpad_and_clip_axis1_64')
    ret_pass = funcC(tostarts, tostops, target, length)
    pytest_tostarts = [0, 3, 6]
    assert tostarts[:len(pytest_tostarts)] == pytest.approx(pytest_tostarts)
    pytest_tostops = [3, 6, 9]
    assert tostops[:len(pytest_tostops)] == pytest.approx(pytest_tostops)
    assert not ret_pass.str

