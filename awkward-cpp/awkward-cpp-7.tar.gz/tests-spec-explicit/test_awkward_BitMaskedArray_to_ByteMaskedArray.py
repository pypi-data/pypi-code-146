import pytest
import kernels

def test_awkward_BitMaskedArray_to_ByteMaskedArray_1():
	tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 2
	frombitmask = [58, 59]
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
	funcPy(tobytemask = tobytemask,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_tobytemask = [0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1]
	assert tobytemask == pytest_tobytemask


def test_awkward_BitMaskedArray_to_ByteMaskedArray_2():
	tobytemask = [123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 1
	frombitmask = [66]
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
	funcPy(tobytemask = tobytemask,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_tobytemask = [0, 1, 0, 0, 0, 0, 1, 0]
	assert tobytemask == pytest_tobytemask


def test_awkward_BitMaskedArray_to_ByteMaskedArray_3():
	tobytemask = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 2
	frombitmask = [58, 59]
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_ByteMaskedArray')
	funcPy(tobytemask = tobytemask,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_tobytemask = [0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0]
	assert tobytemask == pytest_tobytemask


