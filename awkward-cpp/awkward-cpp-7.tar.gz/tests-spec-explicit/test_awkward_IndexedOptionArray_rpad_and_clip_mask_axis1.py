import pytest
import kernels

def test_awkward_IndexedOptionArray_rpad_and_clip_mask_axis1_1():
	toindex = [123, 123, 123, 123]
	frommask = [0, 0, 0, 0]
	length = 4
	funcPy = getattr(kernels, 'awkward_IndexedOptionArray_rpad_and_clip_mask_axis1')
	funcPy(toindex = toindex,frommask = frommask,length = length)
	pytest_toindex = [0, 1, 2, 3]
	assert toindex == pytest_toindex


