import pytest
import kernels

def test_awkward_RegularArray_broadcast_tooffsets_1():
	fromoffsets = [0, 2, 4, 6]
	offsetslength = 4
	size = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_2():
	fromoffsets = [0, 3]
	offsetslength = 2
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_3():
	fromoffsets = [0, 3, 6]
	offsetslength = 3
	size = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_4():
	fromoffsets = [0, 4]
	offsetslength = 2
	size = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_5():
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	offsetslength = 7
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_6():
	fromoffsets = [0, 5, 10, 15, 20]
	offsetslength = 5
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_7():
	fromoffsets = [0, 5]
	offsetslength = 2
	size = 5
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


def test_awkward_RegularArray_broadcast_tooffsets_8():
	fromoffsets = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63, 70, 77, 84, 91, 98, 105, 112, 119, 126, 133, 140, 147, 154, 161, 168, 175, 182, 189, 196, 203, 210]
	offsetslength = 31
	size = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets')
	funcPy(fromoffsets = fromoffsets,offsetslength = offsetslength,size = size)


