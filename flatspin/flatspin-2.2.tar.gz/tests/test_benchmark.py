import numpy as np
import pytest
import time

from flatspin import SquareSpinIceClosed

def test_init(benchmark, opencl):
    size = (10,10)

    def init():
        model = SquareSpinIceClosed(size=size, neighbor_distance=10, **opencl)
        model.dipolar_fields() # Ensure h_dip_cache initialized

    benchmark(init)

@pytest.mark.parametrize("neighbor_distance", [1,5,10,20])
def test_neighbor_distance(benchmark, opencl, neighbor_distance):
    size = (20,20)

    init = lambda: SquareSpinIceClosed(size=size, neighbor_distance=neighbor_distance, **opencl)

    benchmark(init)

def test_dipolar_fields(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.dipolar_fields)

def test_external_fields(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.external_fields)

def test_total_fields(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.total_fields)

def test_flippable(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, hc=0.04, **opencl)
    si.randomize()

    benchmark(si.flippable)

def test_step(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, hc=0.04, **opencl)

    def step():
        si.randomize()

    benchmark(step)

def test_relax(benchmark, opencl):
    size = (50,50)
    si = SquareSpinIceClosed(size=size, hc=0.04, **opencl)

    def relax():
        si.randomize()
        si.relax()

    benchmark(relax)

def test_energy(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.energy)

def test_total_energy(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.total_energy)

def test_total_magnetization(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.total_magnetization)

def test_vertices(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    vertices = lambda: list(si.vertices())

    benchmark(vertices)

def test_vertex_count(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.vertex_count)

def test_vertex_population(benchmark, opencl):
    size = (100,100)
    si = SquareSpinIceClosed(size=size, **opencl)
    si.randomize()

    benchmark(si.vertex_population)

def test_spin_grid(benchmark):
    size = (100,100)
    si = SquareSpinIceClosed(size=size)
    si.randomize()

    benchmark(si.spin_grid)

def test_update_thermal_noise(benchmark):
    size = (25, 25)
    si = SquareSpinIceClosed(size=size, temperature=300)
    si.randomize()

    benchmark(si.update_thermal_noise)

def test_set_angle(benchmark, opencl):
    size = (10,10)
    model = SquareSpinIceClosed(size=size, neighbor_distance=10, **opencl)
    model.dipolar_fields() # Ensure h_dip_cache initialized
    angle = np.random.uniform(0, 360, model.spin_count)
    angle = np.deg2rad(angle)

    def set_angle():
        model.set_angle(angle)
        model.dipolar_fields() # Ensure h_dip_cache initialized

    benchmark(set_angle)

def test_set_pos(benchmark, opencl):
    size = (10,10)
    model = SquareSpinIceClosed(size=size, neighbor_distance=10, **opencl)
    model.dipolar_fields() # Ensure h_dip_cache initialized
    pos = model.pos + .3*np.random.uniform(-1, 1, model.pos.shape)

    def set_pos():
        model.set_pos(pos)
        model.dipolar_fields() # Ensure h_dip_cache initialized

    benchmark(set_pos)

def test_set_geometry(benchmark, opencl):
    size = (10,10)
    model = SquareSpinIceClosed(size=size, neighbor_distance=10, **opencl)
    model.dipolar_fields() # Ensure h_dip_cache initialized
    pos = model.pos + .3*np.random.uniform(-1, 1, model.pos.shape)
    angle = np.random.uniform(0, 360, model.spin_count)
    angle = np.deg2rad(angle)

    def set_geometry():
        model.set_geometry(pos, angle)
        model.dipolar_fields() # Ensure h_dip_cache initialized

    benchmark(set_geometry)
