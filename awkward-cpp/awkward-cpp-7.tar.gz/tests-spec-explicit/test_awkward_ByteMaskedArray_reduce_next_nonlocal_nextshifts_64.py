import pytest
import kernels

def test_awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64_1():
	nextshifts = [123, 123, 123, 123, 123]
	length = 7
	mask = [0, 0, 0, 1, 1, 0, 0]
	valid_when = False
	funcPy = getattr(kernels, 'awkward_ByteMaskedArray_reduce_next_nonlocal_nextshifts_64')
	funcPy(nextshifts = nextshifts,length = length,mask = mask,valid_when = valid_when)
	pytest_nextshifts = [0, 0, 0, 2, 2]
	assert nextshifts == pytest_nextshifts


