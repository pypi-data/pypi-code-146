import pytest
import kernels

def test_awkward_ByteMaskedArray_overlay_mask_1():
	tomask = [123, 123]
	length = 2
	mymask = [0, 0]
	theirmask = [0, 0]
	validwhen = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_overlay_mask')
	funcPy(tomask = tomask,length = length,mymask = mymask,theirmask = theirmask,validwhen = validwhen)
	pytest_tomask = [0, 0]
	assert tomask == pytest_tomask


