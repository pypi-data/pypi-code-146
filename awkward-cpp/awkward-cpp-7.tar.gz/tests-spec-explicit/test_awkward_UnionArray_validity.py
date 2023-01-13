import pytest
import kernels

def test_awkward_UnionArray_validity_1():
	index = [0, 1, 2, 3, 0, 1]
	lencontents = [4, 2, 0, 945]
	length = 6
	numcontents = 2
	tags = [0, 0, 0, 0, 1, 1]
	funcPy = getattr(kernels, 'awkward_UnionArray_validity')
	funcPy(index = index,lencontents = lencontents,length = length,numcontents = numcontents,tags = tags)


def test_awkward_UnionArray_validity_2():
	index = [0, 1, 2, 0, 1, 2, 3]
	lencontents = [3, 4]
	length = 7
	numcontents = 2
	tags = [0, 0, 0, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_UnionArray_validity')
	funcPy(index = index,lencontents = lencontents,length = length,numcontents = numcontents,tags = tags)


def test_awkward_UnionArray_validity_3():
	index = [0, 1, 0, 1, 2, 3]
	lencontents = [2, 4, 32, 49, 0, 0]
	length = 6
	numcontents = 2
	tags = [0, 0, 1, 1, 1, 1]
	funcPy = getattr(kernels, 'awkward_UnionArray_validity')
	funcPy(index = index,lencontents = lencontents,length = length,numcontents = numcontents,tags = tags)


def test_awkward_UnionArray_validity_4():
	index = [0, 0, 1, 1, 2, 3, 2, 4]
	lencontents = [5, 3, 32, 33]
	length = 8
	numcontents = 2
	tags = [0, 1, 1, 0, 0, 0, 1, 0]
	funcPy = getattr(kernels, 'awkward_UnionArray_validity')
	funcPy(index = index,lencontents = lencontents,length = length,numcontents = numcontents,tags = tags)


def test_awkward_UnionArray_validity_5():
	index = [0, 0, 1, 1, 2, 3, 2, 4]
	lencontents = [5, 3, 32, 625, 0, 0, 0]
	length = 8
	numcontents = 2
	tags = [0, 1, 1, 0, 0, 0, 1, 0]
	funcPy = getattr(kernels, 'awkward_UnionArray_validity')
	funcPy(index = index,lencontents = lencontents,length = length,numcontents = numcontents,tags = tags)


def test_awkward_UnionArray_validity_6():
	index = [0, 0, 1, 1, 2, 2, 3]
	lencontents = [3, 4, 32, 177]
	length = 7
	numcontents = 2
	tags = [0, 1, 1, 0, 0, 1, 1]
	funcPy = getattr(kernels, 'awkward_UnionArray_validity')
	funcPy(index = index,lencontents = lencontents,length = length,numcontents = numcontents,tags = tags)


