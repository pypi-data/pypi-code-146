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

def test_pyawkward_ListArray64_getitem_jagged_expand_64_1():
    multistarts = [123, 123, 123]
    multistops = [123, 123, 123]
    singleoffsets = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    tocarry = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    jaggedsize = 1
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_expand_64')
    funcPy(multistarts=multistarts, multistops=multistops, singleoffsets=singleoffsets, tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, jaggedsize=jaggedsize, length=length)
    pytest_multistarts = [1, 1, 1]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [1, 1, 1]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_expand_64_2():
    multistarts = [123, 123, 123]
    multistops = [123, 123, 123]
    singleoffsets = [2, 3, 3, 4, 5, 5, 5, 5, 5, 6, 7, 8, 10, 11]
    tocarry = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    jaggedsize = 1
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_expand_64')
    funcPy(multistarts=multistarts, multistops=multistops, singleoffsets=singleoffsets, tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, jaggedsize=jaggedsize, length=length)
    pytest_multistarts = [2, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [3, 3, 3]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_expand_64_3():
    multistarts = [123, 123, 123]
    multistops = [123, 123, 123]
    singleoffsets = [2, 1, 0, 1, 2, 0, 1, 2, 2, 2, 1, 2, 1, 0, 0, 0, 0]
    tocarry = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    jaggedsize = 1
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_expand_64')
    funcPy(multistarts=multistarts, multistops=multistops, singleoffsets=singleoffsets, tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, jaggedsize=jaggedsize, length=length)
    pytest_multistarts = [2, 2, 2]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [1, 1, 1]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_expand_64_4():
    multistarts = [123, 123, 123]
    multistops = [123, 123, 123]
    singleoffsets = [1, 0, 2, 3, 1, 2, 0, 0, 1, 1, 2, 3, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    tocarry = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    jaggedsize = 1
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_expand_64')
    funcPy(multistarts=multistarts, multistops=multistops, singleoffsets=singleoffsets, tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, jaggedsize=jaggedsize, length=length)
    pytest_multistarts = [1, 1, 1]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 0, 0]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

def test_pyawkward_ListArray64_getitem_jagged_expand_64_5():
    multistarts = [123, 123, 123]
    multistops = [123, 123, 123]
    singleoffsets = [0, 0, 0, 0, 0, 0, 0, 0]
    tocarry = [123, 123, 123]
    fromstarts = [0, 0, 0, 0, 0, 0, 0, 0]
    fromstops = [1, 1, 1, 1, 1, 1, 1, 1]
    jaggedsize = 1
    length = 3
    funcPy = getattr(kernels, 'awkward_ListArray64_getitem_jagged_expand_64')
    funcPy(multistarts=multistarts, multistops=multistops, singleoffsets=singleoffsets, tocarry=tocarry, fromstarts=fromstarts, fromstops=fromstops, jaggedsize=jaggedsize, length=length)
    pytest_multistarts = [0, 0, 0]
    assert multistarts[:len(pytest_multistarts)] == pytest.approx(pytest_multistarts)
    pytest_multistops = [0, 0, 0]
    assert multistops[:len(pytest_multistops)] == pytest.approx(pytest_multistops)
    pytest_tocarry = [0, 0, 0]
    assert tocarry[:len(pytest_tocarry)] == pytest.approx(pytest_tocarry)

