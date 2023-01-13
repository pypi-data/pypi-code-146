import pytest
import kernels

def test_awkward_ListArray_getitem_next_range_counts_1():
	total = [123]
	fromoffsets = [0, 2, 2, 4, 4, 5, 6, 7, 9, 9]
	lenstarts = 9
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [9]
	assert total == pytest_total


def test_awkward_ListArray_getitem_next_range_counts_2():
	total = [123]
	fromoffsets = [0, 2, 4, 5, 6, 7, 9]
	lenstarts = 6
	funcPy = getattr(kernels, 'awkward_ListArray_getitem_next_range_counts')
	funcPy(total = total,fromoffsets = fromoffsets,lenstarts = lenstarts)
	pytest_total = [9]
	assert total == pytest_total


