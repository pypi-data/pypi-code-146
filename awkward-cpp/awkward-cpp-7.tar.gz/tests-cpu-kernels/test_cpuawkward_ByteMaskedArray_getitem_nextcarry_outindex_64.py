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

def test_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_1():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0.0, 1.0, 2.0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_2():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [0, 0, 0, 0, 0]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = False
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0.0, 1.0, 2.0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_3():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0.0, 1.0, 2.0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

def test_cpuawkward_ByteMaskedArray_getitem_nextcarry_outindex_64_4():
    tocarry = [123, 123, 123]
    tocarry = (ctypes.c_int64*len(tocarry))(*tocarry)
    outindex = [123, 123, 123]
    outindex = (ctypes.c_int64*len(outindex))(*outindex)
    mask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    mask = (ctypes.c_int8*len(mask))(*mask)
    length = 3
    validwhen = True
    funcC = getattr(lib, 'awkward_ByteMaskedArray_getitem_nextcarry_outindex_64')
    ret_pass = funcC(tocarry, outindex, mask, length, validwhen)
    pytest_tocarry = [0, 1, 2]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)
    pytest_outindex = [0.0, 1.0, 2.0]
    assert outindex[:len(pytest_outindex)] == pytest.approx(pytest_outindex)
    assert not ret_pass.str

