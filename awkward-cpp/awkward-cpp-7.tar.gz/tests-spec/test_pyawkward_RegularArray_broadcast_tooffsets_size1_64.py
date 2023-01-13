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

def test_pyawkward_RegularArray_broadcast_tooffsets_size1_64_1():
    tocarry = [123]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    offsetslength = 3
    funcPy = getattr(kernels, 'awkward_RegularArray_broadcast_tooffsets_size1_64')
    funcPy(tocarry=tocarry, fromoffsets=fromoffsets, offsetslength=offsetslength)
    pytest_tocarry = [0.0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

