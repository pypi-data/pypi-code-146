import numpy as np
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal
from itertools import groupby

from flatspin import TileLatticeSpinIce

def test_init(opencl):
    b0, b1 = [1,0], [0,1]
    a=0.5
    hole_tile = [(1,0), (1,1)]
    angle_tile = (0, 90)
    size = (3,3)
    si = TileLatticeSpinIce(size=size, lattice_spacing=a, basis0=b0, basis1=b1, const_angle=45, radians=False,
                             hole_tile=hole_tile, angle_tile=angle_tile, **opencl)

    assert si.size == (3,3)
    assert si.spin_count == 7
    assert si.num_neighbors == 3

    assert_array_equal(si.pos, np.array([[0. , 0. ],
                                         [1. , 0. ],
                                         [0. , 0.5],
                                         [0.5, 0.5],
                                         [1. , 0.5],
                                         [0. , 1. ],
                                         [1. , 1. ]]))
    assert_array_equal(si.angle, [0, 0, 0, np.deg2rad(90), 0, 0, 0])

def test_geometry():
    #test square lattice
    b0, b1 = [1,0], [0,1]
    angle_tile = ((90 + 45, 45), (45, 90 + 45))
    si = TileLatticeSpinIce(size=(3,3), basis0=b0, basis1=b1, radians=False, angle_tile=angle_tile)
    assert_array_equal(si.pos, np.array([[0, 0],
                                         [1, 0],
                                         [2, 0],
                                         [0, 1],
                                         [1, 1],
                                         [2, 1],
                                         [0, 2],
                                         [1, 2],
                                         [2, 2]]))
    assert_array_equal(si.angle, np.deg2rad([135, 45, 135, 45, 135, 45, 135, 45, 135]))

    #test kagome lattice
    b0, b1 = [1,0], [0.5, np.sin(np.deg2rad(60))]
    angle_tile = (30, -30), (90, 90)
    hole_tile = ((1,1),(1,0))
    si = TileLatticeSpinIce(size=(4,3), basis0=b0, basis1=b1, radians=False, angle_tile=angle_tile, hole_tile=hole_tile)
    sin60 = np.sin(np.deg2rad(60))
    assert_array_equal(si.pos, np.array([[0, 0],
                                         [1, 0],
                                         [2, 0],
                                         [3, 0],
                                         [0.5, sin60],
                                         [2.5, sin60],
                                         [1, 2 * sin60],
                                         [2, 2 * sin60],
                                         [3, 2 * sin60],
                                         [4, 2 * sin60]]))
    assert_array_equal(si.angle, np.deg2rad([30, -30, 30, -30, 90, 90, 30, -30, 30, -30]))


def test_labels():
    si = TileLatticeSpinIce(size=(2,2))
    assert_array_equal(si.labels,
            [[0, 0],[1, 0],
             [0, 1],[1, 1]])
    si = TileLatticeSpinIce(size=(3,3), hole_tile=(1, 0))
    assert_array_equal(si.labels,
            [[0, 0],
             [2, 0],
             [0, 1],
             [2, 1],
             [0, 2],
             [2, 2]])


def test_indexof():
    si = TileLatticeSpinIce(size=(4,4), hole_tile=((1,1),(0,0)))

    inds = [si.indexof(tuple(l)) for l in si.labels]
    assert_array_equal(inds, si.indices())

def test_set_angle_tile(opencl):
    b0, b1 = [1,0], [0,1]
    a=0.5
    hole_tile = [(1,0), (1,1)]
    angle_tile = (0, 90)
    size = (3,3)
    si = TileLatticeSpinIce(size=size, lattice_spacing=a, basis0=b0, basis1=b1, const_angle=45, radians=False,
                             hole_tile=hole_tile, angle_tile=angle_tile, **opencl)

    assert si.size == (3,3)
    assert si.spin_count == 7
    assert si.num_neighbors == 3

    assert_array_equal(si.angle, [0, 0, 0, np.deg2rad(90), 0, 0, 0])

    angle_tile = (15, 30)
    si.set_angle_tile(angle_tile, radians=False)

    a15 = np.deg2rad(15)
    a30 = np.deg2rad(30)
    assert_array_equal(si.angle, [a15, a15, a15, a30, a15, a15, a15])

    angle_tile = (a30, a15)
    si.set_angle_tile(angle_tile)
    assert_array_equal(si.angle, [a30, a30, a30, a15, a30, a30, a30])


    si.set_angle_tile(None)
    assert_array_equal(si.angle, si.const_angle)

def test_num_neighbors():
    size = (10,10)

    # nearest neighborhood (default)
    si = TileLatticeSpinIce(size=size, hole_tile=(1,0))
    assert si.num_neighbors == 2

    # global neighborhood
    si = TileLatticeSpinIce(size=size, hole_tile=(1,0), neighbor_distance=np.inf)
    assert si.num_neighbors == si.spin_count - 1


def test_neighbors():
    si = TileLatticeSpinIce(size=(6,6), basis0=[0.1,0.9], basis1=[0.9, 0], angle_tile=((0,45,90),(45,90,0)),
                            hole_tile=((1,1),(1,0),(0,1)))
    L = si.L

    # First "horizontal" row
    i = L[0,0]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 0], L[0, 1]}

    i = L[0,1]
    ns = set(si.neighbors(i))
    assert ns == {L[0, 0]}

    # First vertical row
    i = L[1,0]
    ns = set(si.neighbors(i))
    assert ns == {L[0, 0], L[2, 0]}

    i = L[1,2]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 3]}

    # Middle "horizontal" row
    i = L[2,0]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 0], L[2, 1], L[3, 0]}

    i = L[2,3]
    ns = set(si.neighbors(i))
    assert ns == {L[1, 3], L[3, 3], L[2, 4]}


def test_spin_dipolar_field(opencl):
    # default lattice spacing = 1 such that NN islands have coupling strength 1.5
    si = TileLatticeSpinIce(size=(6,6), basis0=[0.1,0.9], basis1=[0.9, 0], angle_tile=((0,45,90),(45,90,0)),
                            hole_tile=((1,1),(1,0),(0,1)))
    L = si.L

    a, b = 0.1767767, 0.53033009
    assert si.spin_dipolar_field(L[0,0], L[0,1]) == approx([1.9399363, -0.96996815])
    assert si.spin_dipolar_field(L[0,0], L[1,0]) == approx([-0.6038843, 2.1832739])

    assert si.spin_dipolar_field(L[0,0], L[2,0]) == approx([0.0554293, 0.3305227])

    assert si.spin_dipolar_field(L[1,0], L[0,0]) == approx([-0.6038843, 1.2309949])
    assert si.spin_dipolar_field(L[1,0], L[0,1]) == approx([-0.5668027, 0.100721])

    assert si.spin_dipolar_field(L[1,2], L[0,1]) == approx([0.8179162, -0.0646619])
    assert si.spin_dipolar_field(L[1,2], L[2,1]) == approx([-0.4720105, -0.734549])
    assert si.spin_dipolar_field(L[1,2], L[0,0]) == approx([0.1986713, -0.0220363])
    assert si.spin_dipolar_field(L[1,2], L[2,0]) == approx([-0.1573542, 0.0891495])

def test_dipolar_field(opencl):
    si = TileLatticeSpinIce(size=(6,6), basis0=[0.1,0.9], basis1=[0.9, 0], angle_tile=((0,45,90),(45,90,0)),
                            hole_tile=((1,1),(1,0),(0,1)), lattice_spacing=0.3, **opencl)
    L = si.L

    assert si.dipolar_field(L[2,0]) == approx([0.09728548, -0.03119054])
    si.flip(L[3,0])
    assert si.dipolar_field(L[2,0]) == approx([0.06443851, -0.12729835])
    si.flip(L[2,1])
    assert si.dipolar_field(L[2,0]) == approx([0.06443851, 0.0759227])

def test_external_field(opencl):
    si = TileLatticeSpinIce(size=(6,6), basis0=[0.1,0.9], basis1=[0.9, 0], angle_tile=((0,45,90),(45,90,0)),
                            hole_tile=((1,1),(1,0),(0,1)), lattice_spacing=0.3, **opencl)
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
    assert si.external_field(L[0,0]) == approx([1.0, 0.0])
    assert si.external_field(L[0,1]) == approx([0.7071068, -0.7071068])
    assert si.external_field(L[1,0]) == approx([0.7071068, -0.7071068])

    # Vertical
    si.set_h_ext((0,1))
    assert si.external_field(L[0,0]) == approx([0.0, 1.0])
    assert si.external_field(L[0,1]) == approx([0.7071068, 0.7071068])
    assert si.external_field(L[1,0]) == approx([0.7071068, 0.7071068])

    # 30 degrees
    si.set_h_ext((cos30, sin30))
    assert si.external_field(L[0,0]) == approx([0.8660254, 0.5])
    assert si.external_field(L[0,1]) == approx([0.9659258, -0.258819])
    assert si.external_field(L[1,0]) == approx([0.9659258, -0.258819])

    # -30 degrees
    si.set_h_ext((np.cos(-a30), np.sin(-a30)))
    assert si.external_field(L[0,0]) == approx([0.8660254, -0.5])
    assert si.external_field(L[0,1]) == approx([0.258819, -0.9659258])
    assert si.external_field(L[1,0]) == approx([0.258819, -0.9659258])

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_flippable(opencl, switching):
    si = TileLatticeSpinIce(size=(6,6), basis0=[0.1,0.9], basis1=[0.9, 0], angle_tile=((0,45,90),(45,90,0)),
                            hole_tile=((1,1),(1,0),(0,1)), switching=switching, lattice_spacing=0.3, alpha=0.01, **opencl)
    if switching == "budrikis":
        assert len(si.flippable()) == 3
    elif switching == "sw":
        assert len(si.flippable()) == 5

    si.flip(si.L[1,2])
    E = si.switching_energy()
    flippable = [i for i in si.indices() if E[i] > 0]
    assert len(flippable) > 0
    assert_array_equal(si.flippable(), flippable)

    si.polarize()
    si.set_h_ext([-20, -20])
    assert len(si.flippable()) == si.spin_count


def test_spin_grid(opencl):
    si = TileLatticeSpinIce(size=(3,3), basis0=[-0.1,0.9], basis1=[0.9, -0.1], angle_tile=((0,45),(90,0)),
                            hole_tile=((0,1)), **opencl)
    # grid_spacing == lattice_spacing
    grid = si.spin_grid()
    assert grid.shape == (1, 3, 2)
    expect = [[[0.70710678, 0.70710678], 
              [1, 0], 
              [0.70710678, 0.70710678]]]

    assert_allclose(grid, np.array(expect))
