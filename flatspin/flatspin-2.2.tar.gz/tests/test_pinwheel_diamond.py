import numpy as np
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal

from flatspin import PinwheelSpinIceDiamond

@pytest.mark.parametrize("spin_angle", [45, -45, 30])
def test_find_vertices(spin_angle):
    si = PinwheelSpinIceDiamond(size=(3,3), spin_angle=spin_angle)
    L = si.L
    vi, vj, indices = si.find_vertices()

    assert_array_equal(vi, [0, 0, 0, 1, 1, 2, 2, 2, 3, 3, 4, 4, 4])
    assert_array_equal(vj, [0, 2, 4, 1, 3, 0, 2, 4, 1, 3, 0, 2, 4])

    assert tuple(indices[0]) == (L[0,0], L[1,0], L[1,1], L[2,0])
    assert tuple(indices[1]) == (L[0,1], L[1,1], L[1,2], L[2,1])
    assert tuple(indices[2]) == (L[0,2], L[1,2], L[1,3], L[2,2])

    assert tuple(indices[3]) == (L[1,1], L[2,0], L[2,1], L[3,1])
    assert tuple(indices[4]) == (L[1,2], L[2,1], L[2,2], L[3,2])

    assert tuple(indices[5]) == (L[2,0], L[3,0], L[3,1], L[4,0])
    assert tuple(indices[6]) == (L[2,1], L[3,1], L[3,2], L[4,1])
    assert tuple(indices[7]) == (L[2,2], L[3,2], L[3,3], L[4,2])

    assert tuple(indices[8]) == (L[3,1], L[4,0], L[4,1], L[5,1])
    assert tuple(indices[9]) == (L[3,2], L[4,1], L[4,2], L[5,2])

    assert tuple(indices[10]) == (L[4,0], L[5,0], L[5,1], L[6,0])
    assert tuple(indices[11]) == (L[4,1], L[5,1], L[5,2], L[6,1])
    assert tuple(indices[12]) == (L[4,2], L[5,2], L[5,3], L[6,2])

@pytest.mark.parametrize("spin_angle", [45, -45, 30])
def test_vertex_type(spin_angle):
    import matplotlib.pylab as plt

    si = PinwheelSpinIceDiamond(size=(2,2), edge='asymmetric', spin_angle=spin_angle)

    vertices = si.vertices()

    # first vertex sublattice
    v = vertices[0]

    # type 1
    si.spin[v] = [1, 1, -1, -1]
    assert si.vertex_type(v) == 1
    si.spin[v] = [-1, -1, 1, 1]
    assert si.vertex_type(v) == 1

    # type 2
    si.spin[v] = [1, 1, 1, 1]
    assert si.vertex_type(v) == 2
    si.spin[v] = [-1, 1, 1, -1]
    assert si.vertex_type(v) == 2
    si.spin[v] = [-1, -1, -1, -1]
    assert si.vertex_type(v) == 2
    si.spin[v] = [1, -1, -1, 1]
    assert si.vertex_type(v) == 2

    # type 3
    si.spin[v] = [-1, 1, 1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [-1, 1, -1, -1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [-1, -1, -1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, 1, -1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, -1, 1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, -1, -1, -1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [-1, -1, 1, -1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, 1, 1, -1]
    assert si.vertex_type(v) == 3

    # type 4
    si.spin[v] = [-1, 1, -1, 1]
    assert si.vertex_type(v) == 4
    si.spin[v] = [1, -1, 1, -1]
    assert si.vertex_type(v) == 4



    # second vertex sublattice
    v = vertices[1]

    # type 1
    si.spin[v] = [1, -1, 1, -1]
    assert si.vertex_type(v) == 1
    si.spin[v] = [-1, 1, -1, 1]
    assert si.vertex_type(v) == 1

    # type 2
    si.spin[v] = [1, 1, 1, 1]
    assert si.vertex_type(v) == 2
    si.spin[v] = [-1, 1, 1, -1]
    assert si.vertex_type(v) == 2
    si.spin[v] = [-1, -1, -1, -1]
    assert si.vertex_type(v) == 2
    si.spin[v] = [1, -1, -1, 1]
    assert si.vertex_type(v) == 2

    # type 3
    si.spin[v] = [-1, 1, 1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [-1, 1, -1, -1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [-1, -1, -1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, 1, -1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, -1, 1, 1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, -1, -1, -1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [-1, -1, 1, -1]
    assert si.vertex_type(v) == 3
    si.spin[v] = [1, 1, 1, -1]
    assert si.vertex_type(v) == 3

    # type 4
    si.spin[v] = [-1, -1, 1, 1]
    assert si.vertex_type(v) == 4
    si.spin[v] = [1, 1, -1, -1]
    assert si.vertex_type(v) == 4
