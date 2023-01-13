import pytest
import kernels

def test_awkward_RegularArray_compact_offsets_1():
	tooffsets = [123, 123]
	length = 1
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 1]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_2():
	tooffsets = [123, 123, 123]
	length = 2
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 1, 2]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_3():
	tooffsets = [123, 123, 123, 123]
	length = 3
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 1, 2, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_4():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	size = 1
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 1, 2, 3, 4, 5, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_5():
	tooffsets = [123, 123, 123, 123]
	length = 3
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 2, 4, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_6():
	tooffsets = [123, 123]
	length = 1
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_7():
	tooffsets = [123, 123, 123]
	length = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_8():
	tooffsets = [123, 123]
	length = 1
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 4]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_9():
	tooffsets = [123, 123, 123, 123, 123, 123, 123]
	length = 6
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 5, 10, 15, 20, 25, 30]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_10():
	tooffsets = [123, 123, 123, 123, 123]
	length = 4
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 5, 10, 15, 20]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_11():
	tooffsets = [123, 123]
	length = 1
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_RegularArray_compact_offsets_12():
	tooffsets = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	length = 30
	size = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_compact_offsets')
	funcPy(tooffsets = tooffsets,length = length,size = size)
	pytest_tooffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	assert tooffsets == pytest_tooffsets


