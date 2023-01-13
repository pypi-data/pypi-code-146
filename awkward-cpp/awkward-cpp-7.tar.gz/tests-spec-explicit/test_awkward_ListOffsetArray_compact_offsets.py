import pytest
import kernels

def test_awkward_ListOffsetArray_compact_offsets_1():
	tooffsets = [123, 123, 123, 123]
	fromoffsets = [3, 3, 4, 6]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 0, 1, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_2():
	tooffsets = [123, 123, 123]
	fromoffsets = [3, 3, 5]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 0, 2]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_3():
	tooffsets = [123, 123, 123]
	fromoffsets = [5, 6, 10]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 1, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_4():
	tooffsets = [123, 123, 123, 123, 123, 123]
	fromoffsets = [3, 5, 5, 5, 5, 9]
	length = 5
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 2, 2, 2, 2, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_5():
	tooffsets = [123, 123, 123]
	fromoffsets = [3, 5, 6]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 2, 3]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_6():
	tooffsets = [123, 123, 123, 123]
	fromoffsets = [1, 4, 4, 6]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 3, 3, 5]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_7():
	tooffsets = [123, 123, 123]
	fromoffsets = [1, 4, 7]
	length = 2
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 3, 6]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_8():
	tooffsets = [123, 123, 123, 123]
	fromoffsets = [11, 14, 17, 20]
	length = 3
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 3, 6, 9]
	assert tooffsets == pytest_tooffsets


def test_awkward_ListOffsetArray_compact_offsets_9():
	tooffsets = [123, 123]
	fromoffsets = [20, 25]
	length = 1
	funcPy = getattr(kernels, 'awkward_ListOffsetArray_compact_offsets')
	funcPy(tooffsets = tooffsets,fromoffsets = fromoffsets,length = length)
	pytest_tooffsets = [0, 5]
	assert tooffsets == pytest_tooffsets


