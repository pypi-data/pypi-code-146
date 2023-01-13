import pytest
import kernels

def test_awkward_RegularArray_getitem_next_range_spreadadvanced_1():
	toadvanced = [123, 123]
	fromadvanced = [0]
	length = 1
	nextsize = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced')
	funcPy(toadvanced = toadvanced,fromadvanced = fromadvanced,length = length,nextsize = nextsize)
	pytest_toadvanced = [0, 0]
	assert toadvanced == pytest_toadvanced


def test_awkward_RegularArray_getitem_next_range_spreadadvanced_2():
	toadvanced = [123, 123, 123, 123]
	fromadvanced = [0, 1]
	length = 2
	nextsize = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_getitem_next_range_spreadadvanced')
	funcPy(toadvanced = toadvanced,fromadvanced = fromadvanced,length = length,nextsize = nextsize)
	pytest_toadvanced = [0, 0, 1, 1]
	assert toadvanced == pytest_toadvanced


