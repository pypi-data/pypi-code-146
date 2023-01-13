import pytest
import kernels

def test_awkward_UnionArray_filltags_1():
	totags = [123, 123, 123, 123, 123, 123]
	base = 0
	fromtags = [0, 0, 0, 1, 1, 1]
	length = 6
	totagsoffset = 0
	funcPy = getattr(kernels, 'awkward_UnionArray_filltags')
	funcPy(totags = totags,base = base,fromtags = fromtags,length = length,totagsoffset = totagsoffset)
	pytest_totags = [0, 0, 0, 1, 1, 1]
	assert totags == pytest_totags


