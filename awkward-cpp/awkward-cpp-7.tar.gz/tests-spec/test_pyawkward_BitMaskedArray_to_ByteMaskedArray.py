# AUTO GENERATED ON 2023-01-12 AT 23:40:21
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import kernels

def test_pyawkward_BitMaskedArray_to_ByteMaskedArray_1():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [1, 1, 1, 1, 1]
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    funcPy(tobytemask=tobytemask, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_tobytemask = [False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)

def test_pyawkward_BitMaskedArray_to_ByteMaskedArray_2():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [0, 0, 0, 0, 0]
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    funcPy(tobytemask=tobytemask, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_tobytemask = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)

def test_pyawkward_BitMaskedArray_to_ByteMaskedArray_3():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    bitmasklength = 3
    validwhen = True
    lsb_order = False
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    funcPy(tobytemask=tobytemask, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_tobytemask = [True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)

def test_pyawkward_BitMaskedArray_to_ByteMaskedArray_4():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    bitmasklength = 3
    validwhen = True
    lsb_order = True
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    funcPy(tobytemask=tobytemask, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_tobytemask = [False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True, False, True, True, True, True, True, True, True]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)

def test_pyawkward_BitMaskedArray_to_ByteMaskedArray_5():
    tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
    frombitmask = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    bitmasklength = 3
    validwhen = False
    lsb_order = False
    funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
    funcPy(tobytemask=tobytemask, frombitmask=frombitmask, bitmasklength=bitmasklength, validwhen=validwhen, lsb_order=lsb_order)
    pytest_tobytemask = [False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, True]
    assert tobytemask[:len(pytest_tobytemask)] == pytest.approx(pytest_tobytemask)

