import numpy as np
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal
from itertools import groupby

from flatspin import LatticeSpinIce

def test_init(opencl):
    b0, b1 = [1,0], [0,1]
    a=0.5
    si = LatticeSpinIce(size=(3,3), lattice_spacing=a, basis0=b0, basis1=b1, const_angle=45, radians=False, **opencl)

    assert si.size == (3,3)
    assert si.spin_count == 3 * 3
    assert si.num_neighbors == 4

    assert_array_equal(si.pos, np.array([[0. , 0. ],
                                        [0.5, 0. ],
                                        [1. , 0. ],
                                        [0. , 0.5],
                                        [0.5, 0.5],
                                        [1. , 0.5],
                                        [0. , 1. ],
                                        [0.5, 1. ],
                                        [1. , 1. ]]))
    assert_array_equal(si.angle, [np.deg2rad(45)] * 9)

    si = LatticeSpinIce(size=(3,3), lattice_spacing=a, basis0=b0, basis1=b1, const_angle=np.pi, radians=True, **opencl)
    assert_array_equal(si.angle, [np.pi] * 9)

def test_labels():
    si = LatticeSpinIce(size=(2,2))
    assert_array_equal(si.labels,
            [[0, 0],[1, 0],
             [0, 1],[1, 1]])
    si = LatticeSpinIce(size=(3,4))
    assert_array_equal(si.labels,
            [[0, 0],[1, 0],[2, 0],
             [0, 1],[1, 1],[2, 1],
             [0, 2],[1, 2],[2, 2],
             [0, 3],[1, 3],[2, 3 ]])

def test_set_basis(opencl):
    b0, b1 = [1,0], [0,1]
    a = 0.5

    params = dict(
            size=(3,3), lattice_spacing=a,
            const_angle=45, radians=False,
            )
    params.update(opencl)

    si = LatticeSpinIce(basis0=b0, basis1=b1, **params)

    # change basis0
    b0_new = [2,1]
    si.set_basis(basis0=b0_new)

    expect = LatticeSpinIce(basis0=b0_new, basis1=b1, **params)
    assert_array_equal(si.pos, expect.pos)
    assert_array_equal(si.angle, expect.angle)

    # change basis1
    b1_new = [-.5,-1]
    si.set_basis(basis1=b1_new)

    expect = LatticeSpinIce(basis0=b0_new, basis1=b1_new, **params)
    assert_array_equal(si.pos, expect.pos)
    assert_array_equal(si.angle, expect.angle)

    # change both basis
    si = LatticeSpinIce(basis0=b0, basis1=b1, **params)
    si.set_basis(b0_new, b1_new)

    expect = LatticeSpinIce(basis0=b0_new, basis1=b1_new, **params)
    assert_array_equal(si.pos, expect.pos)
    assert_array_equal(si.angle, expect.angle)

def test_indexof():
    si = LatticeSpinIce(size=(4,3))

    inds = [si.indexof(tuple(l)) for l in si.labels]
    assert_array_equal(inds, si.indices())


def test_num_neighbors():
    size = (10,10)

    # nearest neighborhood (default)
    si = LatticeSpinIce(size=size)
    assert si.num_neighbors == 4

    # global neighborhood
    si = LatticeSpinIce(size=size, neighbor_distance=np.inf)
    assert si.num_neighbors == si.spin_count - 1


def test_neighbors():
    size=(3,3)
    si = LatticeSpinIce(size=size, basis0=[0.1,0.9], basis1=[-0.1,0.9])
    L = si.L

    # First "horizontal" row
    i = L[0,0]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 0], L[0, 1]}

    i = L[0,1]
    ns = set(si.neighbors(i))
    assert ns == {L[0, 0], L[1, 0], L[2, 0], L[1, 1], L[0, 2]}

    # First vertical row
    i = L[1,0]
    ns = set(si.neighbors(i))
    assert ns == {L[0, 0], L[2, 0], L[0, 1], L[1, 1], L[0, 2]}

    i = L[1,1]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 0], L[2, 0], L[0, 1], L[2, 1], L[0, 2], L[1, 2]}

    i = L[1,2]
    ns = set(si.neighbors(i))
    assert ns == {L[2, 0], L[1, 1], L[2, 1], L[0, 2], L[2, 2]}

    # Middle "horizontal" row
    i = L[2,0]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 0], L[0, 1], L[1, 1], L[2, 1], L[0, 2], L[1, 2]}

    i = L[2,2]
    ns = set(si.neighbors(i))
    assert ns == {L[2,1], L[1,2]}


def test_spin_dipolar_field(opencl):
    # default lattice spacing = 1 such that NN islands have coupling strength 1.5
    size = (3,3)
    si = LatticeSpinIce(size=size, basis0=(1, 0), basis1=(0, 1), const_angle=0, **opencl)
    L = si.L

    a, b = 0.1767767, 0.53033009
    assert si.spin_dipolar_field(L[0,0], L[0,1]) == approx([-1, 0])
    assert si.spin_dipolar_field(L[0,0], L[1,0]) == approx([2, 0])
    assert si.spin_dipolar_field(L[0,0], L[1,1]) == approx([a,  b])
    assert si.spin_dipolar_field(L[0,0], L[2,0]) == approx([0.25, 0])

    assert si.spin_dipolar_field(L[1,0], L[0,0]) == approx([2, 0])
    assert si.spin_dipolar_field(L[1,0], L[0,1]) == approx([a, -b])

    assert si.spin_dipolar_field(L[1,1], L[0,1]) == approx([2, 0])
    assert si.spin_dipolar_field(L[1,1], L[0,2]) == approx([a, -b])
    assert si.spin_dipolar_field(L[1,1], L[2,1]) == approx([2, 0])
    assert si.spin_dipolar_field(L[1,1], L[2,2]) == approx([a, b])
    assert si.spin_dipolar_field(L[1,1], L[0,0]) == approx([a, b])
    assert si.spin_dipolar_field(L[1,1], L[2,0]) == approx([a, -b])

def test_dipolar_field(opencl):
    size = (3,3)
    si = LatticeSpinIce(size=size, alpha=1.0, neighbor_distance=1.5, basis0=(1, 0), basis1=(0, 1), const_angle=0, **opencl)
    L = si.L

    assert si.dipolar_field(L[1,1]) == approx([2.70710678, 0])
    si.flip(L[2,1])
    assert si.dipolar_field(L[1,1]) == approx([-1.29289322, 0])
    si.flip(L[0,2])
    assert si.dipolar_field(L[1,1]) == approx([-1.64644661,  1.06066017])

def test_external_field(opencl):
    size = (3,3)
    si = LatticeSpinIce(size=size, neighbor_distance=1, basis0=(1, 0), basis1=(0, 0.5), const_angle=30, **opencl)
    L = si.L
    a30 = np.deg2rad(30)
    cos30 = np.cos(a30)
    sin30 = np.sin(a30)
    cos60 = np.cos(np.deg2rad(60))
    sin60 = np.sin(np.deg2rad(60))

    assert si.external_field(L[0,0]) == approx([0, 0])
    assert si.external_field(L[1,0]) == approx([0, 0])

    # Horizontal
    si.set_h_ext((1,0))
    assert si.external_field(L[0,0]) == approx([cos30, -sin30])
    assert si.external_field(L[0,1]) == approx([cos30, -sin30])
    assert si.external_field(L[1,0]) == approx([cos30, -sin30])

    # Vertical
    si.set_h_ext((0,1))
    assert si.external_field(L[0,0]) == approx([sin30, cos30])
    assert si.external_field(L[0,1]) == approx([sin30, cos30])
    assert si.external_field(L[1,0]) == approx([sin30, cos30])

    # 30 degrees
    si.set_h_ext((cos30, sin30))
    assert si.external_field(L[0,0]) == approx([1, 0])
    assert si.external_field(L[0,1]) == approx([1, 0])
    assert si.external_field(L[1,0]) == approx([1, 0])

    # -30 degrees
    si.set_h_ext((np.cos(-a30), np.sin(-a30)))
    assert si.external_field(L[0,0]) == approx([sin30, -cos30])
    assert si.external_field(L[0,1]) == approx([sin30, -cos30])
    assert si.external_field(L[1,0]) == approx([sin30, -cos30])

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_flippable(opencl, switching):
    size = (4,3)
    si = LatticeSpinIce(size=size, neighbor_distance=1, basis0=(1, 0), basis1=(0, 0.5), const_angle=30, alpha=1.0, hc=1, switching=switching, **opencl)

    if switching == "budrikis":
        assert len(si.flippable()) == 8
    elif switching == "sw":
        assert len(si.flippable()) == 8

    si.flip(si.L[2,2])
    E = si.switching_energy()
    flippable = [i for i in si.indices() if E[i] > 0]
    assert len(flippable) > 0
    assert_array_equal(si.flippable(), flippable)

    si.polarize()
    si.set_h_ext([-20, 0])
    assert len(si.flippable()) == si.spin_count


def test_spin_grid(opencl):
    ls = 1/2
    si = LatticeSpinIce(size=(2,2), lattice_spacing=ls, **opencl)

    a30 = np.deg2rad(30)
    a90 = np.deg2rad(90)
    v30n = [-np.sin(-a30), -np.cos(-a30)]
    v30p = [np.sin(a30), np.cos(a30)]
    v90 = [1, 0]
    v0 = [0, 0]

    # grid_spacing == lattice_spacing
    grid = si.spin_grid()
    assert grid.shape == (2, 2, 2)
    expect = [[[1, 0], [1, 0]],
              [[1, 0], [1, 0]]]

    assert_allclose(grid, np.array(expect))
