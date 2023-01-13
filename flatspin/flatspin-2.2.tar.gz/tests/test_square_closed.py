import numpy as np
import pytest
from .utils import approx, assert_allclose
from numpy.testing import assert_array_equal

from flatspin import SquareSpinIceClosed

def test_init(opencl):
    si = SquareSpinIceClosed(size=(5,4), **opencl)
    N = 5 * 5 + 4 * 6

    assert si.size == (5, 4)
    assert si.spin_count == N
    assert si.num_neighbors == 8

    si = SquareSpinIceClosed(size=(2,2), init="ground", **opencl) #check groundstate init
    assert_array_equal(si.spin, [ 1, -1, -1,  1, -1, -1,  1,  1, -1,  1,  1, -1])


def test_labels():
    si = SquareSpinIceClosed(size=(2,2))
    assert_array_equal(si.labels,
            [(0,0), (0,1),
             (1,0), (1,1), (1,2),
             (2,0), (2,1),
             (3,0), (3,1), (3,2),
             (4,0), (4,1)])

def test_indexof():
    si = SquareSpinIceClosed(size=(2,2))

    inds = [si.indexof(tuple(l)) for l in si.labels]
    assert_array_equal(inds, si.indices())

    # row 1
    assert_array_equal(si.L[1], [2, 3, 4])

    # col 1
    assert_array_equal(si.L[:,1], [1, 3, 6, 8, 11])

    # every other row
    assert_array_equal(si.L[::2], [0, 1, 5, 6, 10, 11])

    # every other column
    assert_array_equal(si.L[:,::2], [0, 2, 4, 5, 7, 9, 10])

def test_geometry():
    si = SquareSpinIceClosed(size=(3,2))
    L = si.L

    i_horiz = L[::2]
    i_vert = L[1::2]

    assert_array_equal(si.angle[i_horiz], 0)
    assert_allclose(si.angle[i_vert], np.pi/2)

    a = si.lattice_spacing
    assert_array_equal(si.pos[i_horiz, 0], a/2 + a*np.tile(np.arange(3), 3))
    assert_array_equal(si.pos[i_horiz, 1], a*np.repeat(np.arange(3), 3))

    assert_array_equal(si.pos[i_vert, 0], a*np.tile(np.arange(4), 2))
    assert_array_equal(si.pos[i_vert, 1], a/2 + a*np.repeat(np.arange(2), 4))

def test_num_neighbors():
    size = (10,10)

    # nearest neighborhood (default)
    si = SquareSpinIceClosed(size=size)
    assert si.num_neighbors == 8

    # global neighborhood
    si = SquareSpinIceClosed(size=size, neighbor_distance=np.inf)
    assert si.num_neighbors == si.spin_count - 1

def test_neighbors():
    size = (3,3)
    si = SquareSpinIceClosed(size=size)
    L = si.L

    # Horizontal lower left corner
    i = L[0,0]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[1,0], L[1,1], L[0,1], L[2,0]])

    # Horizontal lower center
    i = L[0,1]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[1,1], L[1,2], L[0,0], L[0,2], L[2,1]])

    # Horizontal lower right corner
    i = L[0,2]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[1,2], L[1,3], L[0,1], L[2,2]])

    # Vertical lower left corner
    i = L[1,0]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[0,0], L[2,0], L[3,0], L[1,1]])

    # Vertical left center
    i = L[1,1]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[0,0], L[0,1], L[2,0], L[2,1], L[3,1], L[1,0], L[1,2]])

    # Vertical lower right corner
    i = L[1,3]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[0,2], L[2,2], L[3,3], L[1,2]])

    # Horizontal left
    i = L[2,0]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[1,0], L[1,1], L[3,0], L[3,1], L[2,1], L[0,0], L[4,0]])

    # Horizontal center
    i = L[2,1]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[1,1], L[1,2], L[3,1], L[3,2], L[2,0], L[2,2], L[0,1], L[4,1]])

    # Horizontal right
    i = L[2,2]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[1,2], L[1,3], L[3,2], L[3,3], L[2,1], L[0,2], L[4,2]])

    # Vertical left
    i = L[3,0]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[2,0], L[4,0], L[1,0], L[5,0], L[3,1]])

    # Vertical left center
    i = L[3,1]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[2,0], L[2,1], L[4,0], L[4,1], L[1,1], L[5,1], L[3,0], L[3,2]])

    # Vertical right
    i = L[3,3]
    ns = list(si.neighbors(i))
    assert set(ns) == set([L[2,2], L[4,2], L[1,3], L[5,3], L[3,2]])

def test_spin_dipolar_field(opencl):
    # set lattice spacing such that NN islands have coupling strength 1.5
    a = 2*np.cos(np.pi/4)
    size = (4,4)
    si = SquareSpinIceClosed(size=size, lattice_spacing=a, **opencl)
    L = si.L

    j_NN = np.asarray([1.5, 0.5])
    j_L = np.asarray([1/np.sqrt(2), 0])
    j_T = np.asarray([1/(2*np.sqrt(2)), 0])

    assert si.spin_dipolar_field(L[2,1], L[3,1]) == approx( (-j_NN[0],  j_NN[1]))
    assert si.spin_dipolar_field(L[2,1], L[3,2]) == approx( j_NN)
    assert si.spin_dipolar_field(L[2,1], L[1,1]) == approx( j_NN)
    assert si.spin_dipolar_field(L[2,1], L[1,2]) == approx( (-j_NN[0],  j_NN[1]))

    assert si.spin_dipolar_field(L[2,1], L[2,2]) == approx( j_L )
    assert si.spin_dipolar_field(L[2,1], L[2,0]) == approx( j_L )

    assert si.spin_dipolar_field(L[2,1], L[0,1]) == approx( (-j_T[0], j_T[1]))
    assert si.spin_dipolar_field(L[2,1], L[4,1]) == approx( (-j_T[0], j_T[1]))

def test_dipolar_field(opencl):
    # set lattice spacing such that NN islands have coupling strength 1.5
    a = 2*np.cos(np.pi/4)
    size = (4,4)
    si = SquareSpinIceClosed(size=size, alpha=1.0, lattice_spacing=a, **opencl)
    L = si.L

    j_NN = np.asarray([1.5, 0.5])
    j_L = np.asarray([1/np.sqrt(2), 0])
    j_T = np.asarray([1/(2*np.sqrt(2)), 0])

    assert si.dipolar_field(L[2,1]) == approx(2*j_L - 2*j_T + [0, 4] * j_NN)
    si.flip(L[2,1])
    assert si.dipolar_field(L[2,1]) == approx(-2*j_L + 2*j_T - [0, 4] * j_NN)

    si.flip(L[3,1])
    assert si.dipolar_field(L[2,1]) == approx(-2*j_L + 2*j_T - [2, 2] * j_NN)
    si.flip(L[1,2])
    assert si.dipolar_field(L[2,1]) == approx(-2*j_L + 2*j_T - [4, 0] *j_NN)

def test_external_field(opencl):
    a = 2*np.cos(np.pi/4)
    size = (4,4)
    si = SquareSpinIceClosed(size=size, lattice_spacing=a, **opencl)
    L = si.L

    assert si.external_field(L[0,0]) == approx([0, 0])
    assert si.external_field(L[1,0]) == approx([0, 0])

    # Horizontal
    si.set_h_ext((1,0))
    assert si.external_field(L[0,0]) == approx([1, 0])
    assert si.external_field(L[1,0]) == approx([0,-1])

    # Vertical
    si.set_h_ext((0,1))
    assert si.external_field(L[0,0]) == approx([0, 1])
    assert si.external_field(L[1,0]) == approx([1, 0])

    # 45 degrees
    si.set_h_ext((1,1))
    assert si.external_field(L[0,0]) == approx([1, 1])
    assert si.external_field(L[1,0]) == approx([1,-1])

def test_total_field(opencl):
    si = SquareSpinIceClosed(size=(4,4), **opencl)
    si.randomize()

    i = si.L[2,2]
    assert tuple(si.total_field(i)) == tuple(si.dipolar_field(i) + si.external_field(i))

def test_dipolar_fields(opencl):
    si = SquareSpinIceClosed(size=(5,3), **opencl)
    si.randomize()

    h_dip = si.dipolar_fields()
    for i in si.indices():
        assert tuple(h_dip[i]) == tuple(si.dipolar_field(i))

def test_external_fields(opencl):
    si = SquareSpinIceClosed(size=(8,5), **opencl)
    si.randomize()

    # global external field
    si.set_h_ext((-1,2))

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
    si = SquareSpinIceClosed(size=(4,4), **opencl)
    si.randomize()

    h_tot = si.total_fields()
    for i in si.indices():
        assert tuple(h_tot[i]) == tuple(si.total_field(i))


@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_flippable(opencl, switching):
    si = SquareSpinIceClosed(size=(4,4), hc=1.0, neighbor_distance=np.inf, switching=switching, **opencl)

    assert len(list(si.flippable())) == 0

    si.flip(si.L[0,0])

    E = si.switching_energy()

    flippable = [i for i in si.indices() if E[i] > 0]
    assert_array_equal(si.flippable(), flippable)

    si.polarize()
    si.set_h_ext([-10, -10])
    assert len(si.flippable()) == si.spin_count

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_alpha(opencl, switching):
    hc = 1.0
    h_ext = -(hc + 1.1)
    si = SquareSpinIceClosed(size=(4,4), alpha=1.0, hc=hc, neighbor_distance=np.inf, switching=switching, h_ext=(h_ext, 0), **opencl)
    h_dip = si.dipolar_fields()
    h_external = si.external_fields()
    h_tot = si.total_fields()
    n_flip = len(si.flippable())

    assert 0 < n_flip < si.spin_count

    # adjust alpha only
    alpha = 0.5
    si = SquareSpinIceClosed(size=(4,4), hc=hc, alpha=alpha, neighbor_distance=np.inf, switching=switching, h_ext=(h_ext, 0), **opencl)
    assert np.all(alpha * h_dip == si.dipolar_fields())
    assert np.all(h_external == si.external_fields())
    assert np.all(alpha * h_dip + h_external == si.total_fields())

    # adjust alpha, rescale hc and h_ext
    alpha = 0.5
    hc *= alpha
    h_ext *= alpha
    si = SquareSpinIceClosed(size=(4,4), hc=hc, alpha=alpha, neighbor_distance=np.inf, switching=switching, h_ext=(h_ext, 0), **opencl)

    assert np.all(alpha * h_dip == si.dipolar_fields())
    assert np.all(alpha * h_external == si.external_fields())
    assert np.all(alpha * h_tot == si.total_fields())
    assert len(si.flippable()) == n_flip

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_relax(opencl, switching):
    si = SquareSpinIceClosed(size=(4,4), alpha=1.0, switching=switching, neighbor_distance=np.inf, hc=1.0, **opencl)
    si.flip(si.L[1,1])
    assert si.relax() > 0
    assert len(si.flippable()) == 0

def test_energy(opencl):
    si = SquareSpinIceClosed(size=(4,4), hc=1.0, **opencl)
    E0 = si.energy()
    si.flip(si.L[0,0])
    E1 = si.energy()
    assert E1[0] > E0[0]

@pytest.mark.parametrize("switching", ["budrikis", "sw"])
def test_total_energy(opencl, switching):
    si = SquareSpinIceClosed(size=(6,5), switching=switching, neighbor_distance=np.inf, hc=1.0, **opencl)

    E = si.total_energy()
    si.flip(si.L[0,0])
    assert si.total_energy() > E

    si.randomize()
    E = si.total_energy()
    while si.step():
        assert si.total_energy() < E
        E = si.total_energy()

def test_find_vertices():
    si = SquareSpinIceClosed(size=(4,4))
    L = si.L
    vi, vj, indices = si.find_vertices()

    assert_array_equal(vi, [1, 1, 1, 3, 3, 3, 5, 5, 5])
    assert_array_equal(vj, [1, 3, 5, 1, 3, 5, 1, 3, 5])

    assert tuple(indices[0]) == (L[1,1], L[2,0], L[2,1], L[3,1])
    assert tuple(indices[1]) == (L[1,2], L[2,1], L[2,2], L[3,2])
    assert tuple(indices[2]) == (L[1,3], L[2,2], L[2,3], L[3,3])

    assert tuple(indices[3]) == (L[3,1], L[4,0], L[4,1], L[5,1])
    assert tuple(indices[4]) == (L[3,2], L[4,1], L[4,2], L[5,2])
    assert tuple(indices[5]) == (L[3,3], L[4,2], L[4,3], L[5,3])

    assert tuple(indices[6]) == (L[5,1], L[6,0], L[6,1], L[7,1])
    assert tuple(indices[7]) == (L[5,2], L[6,1], L[6,2], L[7,2])
    assert tuple(indices[8]) == (L[5,3], L[6,2], L[6,3], L[7,3])

def test_vertex_type():
    si = SquareSpinIceClosed(size=(4,4))
    spin = [1, 1, 1, 1, # horiz
            1, 1, -1, 1, 1, # vert
            -1, 1, 1, -1, # horiz
            1, -1, -1, 1, 1, # vert
            -1, 1, -1, -1, # horiz
            1, 1, 1, 1, 1, # vert
            1, 1, 1, -1, # horiz
            1, -1, 1, -1, 1, # vert
            1, 1, 1, 1] # horiz
    si.set_spin(spin)

    vertex = si.vertices()

    assert si.vertex_type(vertex[0]) == 1
    assert si.vertex_type(vertex[1]) == 2
    assert si.vertex_type(vertex[2]) == 3
    assert si.vertex_type(vertex[3]) == 4
    assert si.vertex_type(vertex[4]) == 1
    assert si.vertex_type(vertex[5]) == 2
    assert si.vertex_type(vertex[6]) == 3
    assert si.vertex_type(vertex[7]) == 2
    assert si.vertex_type(vertex[8]) == 4

def test_spin_grid(opencl):
    si = SquareSpinIceClosed(size=(2,1), **opencl)
    spin = [-1, 1,
            1, -1, 1,
            1, -1]
    si.set_spin(spin)

    # grid_spacing == lattice_spacing
    grid = si.spin_grid()
    assert grid.shape == (3, 5, 2)
    expect = [[[0,0], [-1,0], [0,0],  [1,0], [0,0]],
              [[0,1],  [0,0], [0,-1], [0,0], [0,1]],
              [[0,0],  [1,0], [0,0], [-1,0], [0,0]]]
    assert_allclose(grid, expect)

    # grid_spacing < lattice_spacing
    grid = si.spin_grid(si.lattice_spacing/4)
    assert grid.shape == (5, 9, 2)
    expect = [[[0,0], [0,0], [-1,0], [0,0], [0,0],  [0,0], [1,0],  [0,0], [0,0]],
              [[0,0], [0,0],  [0,0], [0,0], [0,0],  [0,0], [0,0],  [0,0], [0,0]],
              [[0,1], [0,0],  [0,0], [0,0], [0,-1], [0,0], [0,0],  [0,0], [0,1]],
              [[0,0], [0,0],  [0,0], [0,0], [0,0],  [0,0], [0,0],  [0,0], [0,0]],
              [[0,0], [0,0],  [1,0], [0,0], [0,0],  [0,0], [-1,0], [0,0], [0,0]]]
    assert_allclose(grid, expect)

    # grid_spacing > lattice_spacing
    grid = si.spin_grid(si.lattice_spacing)
    assert grid.shape == (2, 3, 2)
    expect = [[[-1,1], [1,-1], [0,1]],
              [[1,0],  [-1,0], [0,0]]]
    assert_allclose(grid, expect)

    # sum of all spins
    grid = si.spin_grid(si.spin_count * si.lattice_spacing)
    assert grid.shape == (1, 1, 2)
    expect = [[[0,1]]]
    assert_allclose(grid, expect)
