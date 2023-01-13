import pytest
import kernels

def test_awkward_RegularArray_broadcast_tooffsets_size1_1():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_2():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 5, 10, 15, 20, 25, 30]
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_3():
	tocarry = [123, 123, 123, 123]
	fromoffsets = [0, 4]
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_4():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 4, 7, 7, 9, 9, 11]
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 0, 1, 1, 1, 3, 3, 5, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_5():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 3, 3]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_6():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 6]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 1, 1, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_7():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 2, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_8():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 8, 8, 10]
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 2, 2, 3, 3, 3, 5, 5]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_9():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 3, 3, 5, 6, 10]
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 0, 2, 2, 3, 4, 4, 4, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_10():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 2, 3]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_11():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 6, 8, 10]
	offsetslength = 6
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_12():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
	offsetslength = 11
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_13():
	tocarry = [123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 2, 4, 6, 8, 10, 12, 13, 14, 15, 16]
	offsetslength = 11
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8, 9]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_14():
	tocarry = [123]
	fromoffsets = [0, 1]
	offsetslength = 2
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_15():
	tocarry = [123, 123]
	fromoffsets = [0, 1, 2]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_16():
	tocarry = [123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 5]
	offsetslength = 3
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 1, 1, 1]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_17():
	tocarry = [123, 123, 123]
	fromoffsets = [0, 1, 2, 3]
	offsetslength = 4
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2]
	assert tocarry == pytest_tocarry


def test_awkward_RegularArray_broadcast_tooffsets_size1_18():
	tocarry = [123, 123, 123, 123, 123, 123]
	fromoffsets = [0, 1, 2, 3, 4, 5, 6]
	offsetslength = 7
	funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1')
	funcPy(tocarry = tocarry,fromoffsets = fromoffsets,offsetslength = offsetslength)
	pytest_tocarry = [0, 1, 2, 3, 4, 5]
	assert tocarry == pytest_tocarry


