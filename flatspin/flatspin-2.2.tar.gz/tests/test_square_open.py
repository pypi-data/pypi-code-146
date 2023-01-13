import numpy as np
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal

from flatspin import SquareSpinIceOpen

def test_init(opencl):
    si = SquareSpinIceOpen(size=(5,4), **opencl)

    assert si.size == (5,4)
    assert si.spin_count == 5 * 4
    assert si.num_neighbors == 8

def test_labels(opencl):
    si = SquareSpinIceOpen(size=(2,4), **opencl)
    assert_array_equal(si.labels,
            [(0,0), (0,1),
             (1,0), (1,1),
             (2,0), (2,1),
             (3,0), (3,1)])

def test_indexof():
    si = SquareSpinIceOpen(size=(3,3))

    inds = [si.indexof(tuple(l)) for l in si.labels]
    assert_array_equal(inds, si.indices())

    # row 1
    assert_array_equal(si.L[1], [3, 4, 5])

    # col 1
    assert_array_equal(si.L[:,1], [1, 4, 7])

    # every other row
    assert_array_equal(si.L[::2], [0, 1, 2, 6, 7, 8])

    # every other column
    assert_array_equal(si.L[:,::2], [0, 2, 3, 5, 6, 8])

def test_geometry():
    si = SquareSpinIceOpen(size=(5,4))
    L = si.L

    # alternating 45 and 135 degrees
    a1 = np.pi/4
    a2 = a1 + np.pi/2

    assert_allclose(si.angle[L[0::2,0::2]], a1)
    assert_allclose(si.angle[L[1::2,1::2]], a1)
    assert_allclose(si.angle[L[0::2,1::2]], a2)
    assert_allclose(si.angle[L[1::2,0::2]], a2)

def test_num_neighbors():
    size = (10,10)

    # nearest neighborhood (default)
    si = SquareSpinIceOpen(size=size)
    assert si.num_neighbors == 8

    # global neighborhood
    si = SquareSpinIceOpen(size=size, neighbor_distance=np.inf)
    assert si.num_neighbors == si.spin_count - 1

def test_neighbors():
    size = (3,3)
    si = SquareSpinIceOpen(size=size)
    L = si.L

    # Lower left corner
    i = L[0,0]
    ns = list(si.neighbors(i))
    assert ns == [L[0,1], L[1,0], L[1,1]]

    # Lower center
    i = L[0,1]
    ns = list(si.neighbors(i))
    assert ns == [L[0,0], L[0,2], L[1,0], L[1,1], L[1,2]]

    # Lower right corner
    i = L[0,2]
    ns = list(si.neighbors(i))
    assert ns == [L[0,1], L[1,1], L[1,2]]

    # Left edge
    i = L[1,0]
    ns = list(si.neighbors(i))
    assert ns == [L[0,0], L[0,1], L[1,1], L[2,0], L[2,1]]

    # Center
    i = L[1,1]
    ns = list(si.neighbors(i))
    assert ns == [L[0,0], L[0,1], L[0,2], L[1,0], L[1,2], L[2,0], L[2,1], L[2,2]]

    # Right edge
    i = L[1,2]
    ns = list(si.neighbors(i))
    assert ns == [L[0,1], L[0,2], L[1,1], L[2,1], L[2,2]]

    # Top left corner
    i = L[2,0]
    ns = list(si.neighbors(i))
    assert ns == [L[1,0], L[1,1], L[2,1]]

    # Top center
    i = L[2,1]
    ns = list(si.neighbors(i))
    assert ns == [L[1,0], L[1,1], L[1,2], L[2,0], L[2,2]]

    # Top right
    i = L[2,2]
    ns = list(si.neighbors(i))
    assert ns == [L[1,1], L[1,2], L[2,1]]

def test_spin_dipolar_field(opencl):
    # default lattice spacing = 1 such that NN islands have coupling strength 1.5
    size = (3,3)
    si = SquareSpinIceOpen(size=size, **opencl)
    L = si.L

    j_NN = np.asarray([1.5, 0.5])
    j_L = np.asarray([1/np.sqrt(2), 0])
    j_T = np.asarray([1/(2*np.sqrt(2)), 0])


    assert si.spin_dipolar_field(L[1,1], L[0,1]) == approx(j_NN)
    assert si.spin_dipolar_field(L[1,1], L[1,0]) == approx(j_NN * [-1, 1])
    assert si.spin_dipolar_field(L[1,1], L[1,2]) == approx(j_NN * [-1, 1])
    assert si.spin_dipolar_field(L[1,1], L[2,1]) == approx(j_NN)

    assert si.spin_dipolar_field(L[1,1], L[0,0]) == approx(j_L)
    assert si.spin_dipolar_field(L[1,1], L[2,2]) == approx(j_L)

    assert si.spin_dipolar_field(L[1,1], L[0,2]) == approx(-j_T)
    assert si.spin_dipolar_field(L[1,1], L[2,0]) == approx(-j_T)

def test_dipolar_field(opencl):
    # default lattice spacing = 1 such that NN islands have coupling strength 1.5
    size = (4,4)
    si = SquareSpinIceOpen(size=size, alpha=1.0, **opencl)
    L = si.L

    j_NN = np.asarray([1.5, 0.5])
    j_L = np.asarray([1/np.sqrt(2), 0])
    j_T = np.asarray([1/(2*np.sqrt(2)), 0])

    assert si.dipolar_field(L[1,1]) == approx(2*j_L - 2*j_T + [0, 4] * j_NN)
    si.flip(L[1,1])
    assert si.dipolar_field(L[1,1]) == approx(-2*j_L + 2*j_T - [0, 4] * j_NN)
    si.flip(L[1,0])
    assert si.dipolar_field(L[1,1]) == approx(-2*j_L + 2*j_T - 2*j_NN)
    si.flip(L[1,2])
    assert si.dipolar_field(L[1,1]) == approx(-2*j_L + 2*j_T - [4, 0] *j_NN)

def test_external_field(opencl):
    a = 2*np.cos(np.pi/4)
    size = (4,4)
    si = SquareSpinIceOpen(size=size, lattice_spacing=a, **opencl)
    L = si.L

    assert si.external_field(L[0,0]) == approx([0, 0])
    assert si.external_field(L[1,0]) == approx([0, 0])

    cos45 = np.cos(np.pi/4)
    sin45 = np.sin(np.pi/4)

    # Horizontal
    si.set_h_ext((1,0))
    assert si.external_field(L[0,0]) == approx([cos45, -sin45])
    assert si.external_field(L[1,0]) == approx([-cos45, -sin45])

    # Vertical
    si.set_h_ext((0,1))
    assert si.external_field(L[0,0]) == approx([cos45, sin45])
    assert si.external_field(L[1,0]) == approx([cos45, -sin45])

    # 45 degrees
    si.set_h_ext((1,1))
    assert si.external_field(L[0,0]) == approx([2*cos45, 0])
    assert si.external_field(L[1,0]) == approx([0, -2*sin45])

def test_total_field(opencl):
    si = SquareSpinIceOpen(size=(4,4), **opencl)
    L = si.L
    si.randomize()

    i = L[2,2]
    assert tuple(si.total_field(i)) == tuple(si.dipolar_field(i) + si.external_field(i))

def test_dipolar_fields(opencl):
    si = SquareSpinIceOpen(size=(5,3), **opencl)
    si.randomize()

    h_dip = si.dipolar_fields()
    for i in si.indices():
        assert tuple(h_dip[i]) == tuple(si.dipolar_field(i))

def test_external_fields(opencl):
    si = SquareSpinIceOpen(size=(8,5), **opencl)
    si.randomize()

    # global external field
    si.set_h_ext((-.2,.1))

    h_ext = si.external_fields()
    for i in si.indices():
        assert tuple(h_ext[i]) == approx(tuple(si.external_field(i)))

    # local external field
    h_ext = np.random.uniform(-10, 10, (si.spin_count, 2))
    si.set_h_ext(h_ext)

    h_ext = si.external_fields()
    for i in si.indices():
        assert tuple(h_ext[i]) == approx(tuple(si.external_field(i)))

def test_total_fields(opencl):
    si = SquareSpinIceOpen(size=(4,4), **opencl)
    si.randomize()

    h_tot = si.total_fields()
    for i in si.indices():
        assert tuple(h_tot[i]) == tuple(si.total_field(i))

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_flippable(opencl, switching):
    si = SquareSpinIceOpen(size=(4,4), alpha=1.0, neighbor_distance=np.inf, switching=switching, hc=1.2, **opencl)
    L = si.L

    expected = 0
    if switching == 'sw':
        expected = 4

    assert len(si.flippable()) == expected

    si.flip(L[1,0])
    E = si.switching_energy()

    flippable = [i for i in si.indices() if E[i] > 0]

    assert_array_equal(si.flippable(), flippable)

    si.polarize()
    si.set_h_ext([0, -10])

    assert len(si.flippable()) == si.spin_count

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_alpha(opencl, switching):
    hc = 1.0
    h_ext = -(hc + 1.1)
    si = SquareSpinIceOpen(size=(4,4), alpha=1.0, neighbor_distance=np.inf, switching=switching, hc=hc, h_ext=(h_ext, 0), **opencl)
    h_dip = si.dipolar_fields()
    h_external = si.external_fields()
    h_tot = si.total_fields()
    n_flip = len(si.flippable())

    assert 0 < n_flip < si.spin_count

    # adjust alpha only
    alpha = 0.5
    si = SquareSpinIceOpen(size=(4,4), neighbor_distance=np.inf, switching=switching, hc=hc, h_ext=(h_ext, 0), alpha=alpha, **opencl)

    assert np.all(alpha * h_dip == si.dipolar_fields())
    assert np.all(h_external == si.external_fields())
    assert_allclose(alpha * h_dip + h_external, si.total_fields())

    # adjust alpha, rescale hc and h_ext
    alpha = 0.5
    hc *= alpha
    h_ext *= alpha
    si = SquareSpinIceOpen(size=(4,4), neighbor_distance=np.inf, switching=switching, hc=hc, h_ext=(h_ext, 0), alpha=alpha, **opencl)

    assert np.all(alpha * h_dip == si.dipolar_fields())
    assert np.all(alpha * h_external == si.external_fields())
    assert np.all(alpha * h_tot == si.total_fields())
    assert len(si.flippable()) == n_flip

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_relax(opencl, switching):
    si = SquareSpinIceOpen(size=(4,4), alpha=1.0, neighbor_distance=np.inf, switching=switching, hc=1.0, **opencl)
    si.flip(si.L[1,1])
    assert si.relax() > 0
    assert len(si.flippable()) == 0

def test_energy(opencl):
    si = SquareSpinIceOpen(size=(4,4), hc=1.0, **opencl)
    E0 = si.energy()
    si.flip(si.L[0,0])
    E1 = si.energy()
    assert E1[0] > E0[0]

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_total_energy(opencl, switching):
    si = SquareSpinIceOpen(size=(6,5), neighbor_distance=np.inf, switching=switching, hc=1.0, **opencl)

    E = si.total_energy()
    si.flip(si.L[0,0])
    assert si.total_energy() > E

    si.randomize()
    E = si.total_energy()
    while si.step():
        assert si.total_energy() < E
        E = si.total_energy()

def test_find_vertices():
    si = SquareSpinIceOpen(size=(4,4))
    L = si.L
    vi, vj, indices = si.find_vertices()

    assert_array_equal(vi, [0, 0, 1, 2, 2])
    assert_array_equal(vj, [0, 2, 1, 0, 2])

    assert tuple(indices[0]) == (L[0,0], L[0,1], L[1,0], L[1,1])
    assert tuple(indices[1]) == (L[0,2], L[0,3], L[1,2], L[1,3])

    assert tuple(indices[2]) == (L[1,1], L[1,2], L[2,1], L[2,2])

    assert tuple(indices[3]) == (L[2,0], L[2,1], L[3,0], L[3,1])
    assert tuple(indices[4]) == (L[2,2], L[2,3], L[3,2], L[3,3])

def test_vertex_type():
    si = SquareSpinIceOpen(size=(4,4))
    spin = [1, -1, 1, 1,
            1, -1, 1, 1,
            1, 1, 1, -1,
            -1, -1, 1, 1]
    si.set_spin(spin)

    vertex = si.vertices()

    assert si.vertex_type(vertex[0]) == 1
    assert si.vertex_type(vertex[1]) == 2
    assert si.vertex_type(vertex[2]) == 3
    assert si.vertex_type(vertex[3]) == 4
    assert si.vertex_type(vertex[4]) == 3

def test_spin_grid(opencl):
    ls = 1/3
    si = SquareSpinIceOpen(size=(4,4), lattice_spacing=ls, **opencl)
    spin = [1, 1, 1, 1,
            1, -1, 1, 1,
            1, 1, 1, -1,
            -1, -1, 1, 1]
    si.set_spin(spin)

    # grid_spacing == lattice_spacing
    grid = si.spin_grid()
    assert grid.shape == (4, 4, 2)
    expect = [[[1,1],  [-1,1],  [1,1],  [-1,1]],
              [[-1,1], [-1,-1], [-1,1], [1,1]],
              [[1,1],  [-1,1],  [1,1],  [1,-1]],
              [[1,-1], [-1,-1], [-1,1], [1,1]]]
    assert_allclose(grid, np.array(expect)*np.cos(np.pi/4))

    # grid_spacing < lattice_spacing
    grid = si.spin_grid(ls / 2)
    assert grid.shape == (7, 7, 2)
    expect = [[[1,1],  [0,0], [-1,1],  [0,0], [1,1],  [0,0], [-1,1]],
              [[0,0],  [0,0], [0,0],   [0,0], [0,0],  [0,0], [0,0]],
              [[-1,1], [0,0], [-1,-1], [0,0], [-1,1], [0,0], [1,1]],
              [[0,0],  [0,0], [0,0],   [0,0], [0,0],  [0,0], [0,0]],
              [[1,1],  [0,0], [-1,1],  [0,0], [1,1],  [0,0], [1,-1]],
              [[0,0],  [0,0], [0,0],   [0,0], [0,0],  [0,0], [0,0]],
              [[1,-1], [0,0], [-1,-1], [0,0], [-1,1], [0,0], [1,1]]]
    assert_allclose(grid, np.array(expect)*np.cos(np.pi/4))

    # grid_spacing > lattice_spacing
    grid = si.spin_grid(2 * ls)
    assert grid.shape == (2, 2, 2)
    expect = [[[-2,2], [0,4]],
              [[0,0], [2,2]]]
    assert_allclose(grid, np.array(expect)*np.cos(np.pi/4))

    # sum of all spins
    grid = si.spin_grid(si.spin_count * ls)
    assert grid.shape == (1, 1, 2)
    expect = [[[0,8]]]
    assert_allclose(grid, np.array(expect)*np.cos(np.pi/4))

def test_flip_mode_max(opencl):
    # With flip_mode=max, the flip order should be the same regardless of the
    # sample resolution of the external field, as long as the field has the
    # same extremes (min/max values)
    def do_test(ts):
        si = SquareSpinIceOpen(size=(4,4), disorder=0.05, neighbor_distance=np.inf,
                flip_mode='max', **opencl)

        H = si.hc/np.cos(np.pi/4)
        t = np.linspace(0, 2*np.pi, ts, endpoint=False)
        h_ext = H*np.sin(t)
        assert max(h_ext) == H

        si.polarize()
        for h in h_ext:
            si.set_h_ext((0, h))
            si.relax()
        return si.spin

    spin1000 = do_test(1024)
    spin100 = do_test(128)
    assert_array_equal(spin100, spin1000)
