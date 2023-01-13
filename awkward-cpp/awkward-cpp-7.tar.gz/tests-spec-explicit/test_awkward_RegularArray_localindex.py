import pytest
import kernels

def test_awkward_RegularArray_localindex_1():
	toindex = [123, 123, 123, 123, 123, 123]
	length = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_localindex')
	funcPy(toindex = toindex,length = length,size = size)
	pytest_toindex = [0, 1, 2, 0, 1, 2]
	assert toindex == pytest_toindex


def test_awkward_RegularArray_localindex_2():
	toindex = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 6
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_localindex')
	funcPy(toindex = toindex,length = length,size = size)
	pytest_toindex = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]
	assert toindex == pytest_toindex


