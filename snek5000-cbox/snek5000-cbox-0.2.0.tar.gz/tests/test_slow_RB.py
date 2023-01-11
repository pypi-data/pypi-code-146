from shutil import rmtree

import pytest

import numpy as np

from snek5000 import load
from snek5000_cbox.solver import Simul


@pytest.mark.slow
def params_RB():

    params = Simul.create_default_params()
    aspect_ratio = 1.0 / 41
    params.prandtl = 1.0
    params.Ra_vert = 1705

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.nproc_min = 2
    params.oper.dim = 2

    nb_elements = 1
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)
    params.oper.nz = int(nb_elements / aspect_ratio)

    Ly = params.oper.Ly
    Lx = params.oper.Lx = Ly / aspect_ratio

    params.oper.x_periodicity = True

    params.oper.mesh_stretch_factor = 0.0

    params.oper.elem.order = params.oper.elem.order_out = 12

    # creation of the coordinates of the points saved by history points
    n1d = 4
    small = Lx / 10

    xs = np.linspace(0, Lx, n1d)
    xs[0] = small
    xs[-1] = Lx - small

    ys = np.linspace(0, Ly, n1d)
    ys[0] = small
    ys[-1] = Ly - small

    coords = [(x, y) for x in xs for y in ys]

    params.output.history_points.coords = coords
    params.oper.max.hist = len(coords) + 1

    params.nek.general.dt = 0.05
    params.nek.general.end_time = 500
    params.nek.general.stop_at = "endTime"
    params.nek.general.target_cfl = 2.0
    params.nek.general.time_stepper = "BDF3"

    params.nek.general.write_control = "runTime"
    params.nek.general.write_interval = 1000

    params.output.history_points.write_interval = 100
    params.output.phys_fields.write_interval_pert_field = 200

    return params


# for an infinite layer of fluid with Pr = 1.0, the onset of convection is at Ra_c = 1708


@pytest.mark.slow
def test_simple_RB_nonconvective_simul():

    params = params_RB()

    params.Ra_vert = 1705

    sim = Simul(params)

    sim.make.exec("run_fg", nproc=4)

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    times = df[df.index_points == 1].time
    t_max = times.max()

    # check a physical result,
    temperature_last = df[df.time == t_max].temperature
    assert temperature_last.abs().max() < 0.45

    # check we do not have convection,
    ux_last = df[df.time == t_max].ux
    assert ux_last.abs().max() < 1e-7  # noise amplitude is 1e-5

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)


@pytest.mark.slow
def test_simple_RB_convective_simul():

    params = params_RB()

    params.Ra_vert = 1750
    params.nek.general.end_time = 2000

    sim = Simul(params)

    sim.make.exec("run_fg", nproc=4)

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    times = df[df.index_points == 1].time
    t_max = times.max()

    # check a physical result,
    temperature_last = df[df.time == t_max].temperature
    assert temperature_last.abs().max() < 0.45

    # check we have convection,
    ux_last = df[df.time == t_max].ux
    assert ux_last.abs().max() > 1e-2  # noise amplitude is 1e-5

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)


@pytest.mark.slow
def test_RB_linear_nonconvective_simul():

    params = params_RB()

    params.Ra_vert = 1705

    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"

    sim = Simul(params)
    sim.make.exec("run_fg", nproc=4)

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    times = df[df.index_points == 1].time
    t_max = times.max()

    # check we do not have convection,
    ux_last = df[df.time == t_max].ux
    assert ux_last.abs().max() < 1e-7  # noise amplitude is 1e-5

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)


@pytest.mark.slow
def test_RB_linear_convective_simul():

    params = params_RB()

    params.Ra_vert = 1750

    params.nek.general.end_time = 2000

    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"

    sim = Simul(params)
    sim.make.exec("run_fg", nproc=4)

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    times = df[df.index_points == 1].time

    t_max = times.max()

    # check we have convection,
    ux_last = df[df.time == t_max].ux
    assert ux_last.abs().max() > 2e-2  # noise amplitude is 1e-5

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)
