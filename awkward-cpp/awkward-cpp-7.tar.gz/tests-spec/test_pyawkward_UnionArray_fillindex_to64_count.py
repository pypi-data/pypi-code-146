# AUTO GENERATED ON 2023-01-12 AT 23:40:21
# DO NOT EDIT BY HAND!
#
# To regenerate file, run
#
#     python dev/generate-tests.py
#

# fmt: off

import pytest
import kernels

def test_pyawkward_UnionArray_fillindex_to64_count_1():
    toindex = [123, 123, 123, 123, 123, 123]
    toindexoffset = 3
    length = 3
    funcPy = getattr(kernels, 'awkward_UnionArray_fillindex_to64_count')
    funcPy(toindex=toindex, toindexoffset=toindexoffset, length=length)
    pytest_toindex = [123, 123, 123, 0.0, 1.0, 2.0]
    assert toindex[:len(pytest_toindex)] == pytest.approx(pytest_toindex)

