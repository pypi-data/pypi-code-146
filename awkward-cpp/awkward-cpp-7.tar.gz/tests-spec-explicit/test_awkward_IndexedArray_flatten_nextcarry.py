import pytest
import kernels

def test_awkward_IndexedArray_flatten_nextcarry_1():
	tocarry = [123, 123]
	fromindex = [0, 1]
	lencontent = 2
	lenindex = 2
	funcPy = getattr(kernels, 'awkward_IndexedArray_flatten_nextcarry')
	funcPy(tocarry = tocarry,fromindex = fromindex,lencontent = lencontent,lenindex = lenindex)
	pytest_tocarry = [0, 1]
	assert tocarry == pytest_tocarry


