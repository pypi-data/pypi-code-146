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

def test_pyawkward_ListOffsetArray64_compact_offsets_64_1():
    tooffsets = [123, 123, 123, 123]
    fromoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray64_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromoffsets=fromoffsets, length=length)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray64_compact_offsets_64_2():
    tooffsets = [123, 123, 123, 123]
    fromoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray64_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromoffsets=fromoffsets, length=length)
    pytest_tooffsets = [0, 1, 1, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray64_compact_offsets_64_3():
    tooffsets = [123, 123, 123, 123]
    fromoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray64_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromoffsets=fromoffsets, length=length)
    pytest_tooffsets = [0, -1, -2, -1]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray64_compact_offsets_64_4():
    tooffsets = [123, 123, 123, 123]
    fromoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray64_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromoffsets=fromoffsets, length=length)
    pytest_tooffsets = [0, -1, 1, 2]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

def test_pyawkward_ListOffsetArray64_compact_offsets_64_5():
    tooffsets = [123, 123, 123, 123]
    fromoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    length = 3
    funcPy = getattr(kernels, 'awkward_ListOffsetArray64_compact_offsets_64')
    funcPy(tooffsets=tooffsets, fromoffsets=fromoffsets, length=length)
    pytest_tooffsets = [0, 0, 0, 0]
    assert tooffsets[:len(pytest_tooffsets)] == pytest.approx(pytest_tooffsets)

