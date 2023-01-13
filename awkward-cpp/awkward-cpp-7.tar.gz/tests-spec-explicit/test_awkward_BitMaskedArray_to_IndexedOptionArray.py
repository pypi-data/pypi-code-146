import pytest
import kernels

def test_awkward_BitMaskedArray_to_IndexedOptionArray_1():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 2
	frombitmask = [58, 59]
	lsb_order = False
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, 1, -1, -1, -1, 5, -1, 7, 8, 9, -1, -1, -1, 13, -1, -1]
	assert toindex == pytest_toindex


def test_awkward_BitMaskedArray_to_IndexedOptionArray_2():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	bitmasklength = 2
	frombitmask = [58, 59]
	lsb_order = True
	validwhen = False
	funcPy = getattr(kernels, 'awkward_BitMaskedArray_to_IndexedOptionArray')
	funcPy(toindex = toindex,bitmasklength = bitmasklength,frombitmask = frombitmask,lsb_order = lsb_order,validwhen = validwhen)
	pytest_toindex = [0, -1, 2, -1, -1, -1, 6, 7, -1, -1, 10, -1, -1, -1, 14, 15]
	assert toindex == pytest_toindex


