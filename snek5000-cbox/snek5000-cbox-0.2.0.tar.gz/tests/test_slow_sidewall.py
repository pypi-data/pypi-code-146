from shutil import rmtree, copyfile

import pytest

import numpy as np

from scipy import stats
from scipy.signal import argrelmax

from snek5000 import load
from snek5000_cbox.solver import Simul


@pytest.mark.slow
def params_SW():

    params = Simul.create_default_params()

    aspect_ratio = 1.0
    params.prandtl = 0.71
    params.Ra_side = 1.86e8

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.nproc_min = 2
    params.oper.dim = 2

    nb_elements = 8
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)

    Ly = params.oper.Ly
    Lx = params.oper.Lx = Ly / aspect_ratio

    params.oper.mesh_stretch_factor = 0.08
    params.oper.elem.order = params.oper.elem.order_out = 10

    n1d = 5
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

    params.nek.general.time_stepper = "BDF3"
    params.nek.general.extrapolation = "OIFS"
    params.nek.general.end_time = 800
    params.nek.general.stop_at = "endTime"
    params.nek.general.target_cfl = 2.0

    params.nek.general.write_control = "runTime"
    params.nek.general.write_interval = 100

    params.output.phys_fields.write_interval_pert_field = 500
    params.output.history_points.write_interval = 10

    return params


def compute_growth_rate(sim):

    coords, df = sim.output.history_points.load()
    df_point = df[df.index_points == 12]
    time = df_point["time"].to_numpy()
    ux = df_point["ux"].to_numpy()
    step = np.where(time > 700)[0][0]
    time = time[step:]
    ux = ux[step:]
    signal = ux

    arg_local_max = argrelmax(signal)
    time_loc_max = time[arg_local_max]
    signal_loc_max = signal[arg_local_max]

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_loc_max, np.log(signal_loc_max)
    )

    return slope


@pytest.mark.slow
def test_SW_nonlinear():

    params = params_SW()

    params.Ra_side = 1.86e8

    sim = Simul(params)

    sim.make.exec("run_fg", nproc=4)

    sim = load(sim.path_run)
    coords, df = sim.output.history_points.load()

    times = df[df.index_points == 12].time
    t_max = times.max()

    # check a physical result: since there is no probe close to the center,
    # the temperature values at the end are > 0.1 and < 0.4

    temperature_last = df[df.time == t_max].temperature

    assert temperature_last.abs().max() < 0.4
    assert temperature_last.abs().max() > 0.1

    growth_rate = compute_growth_rate(sim)

    assert 0.0049 < growth_rate < 0.0058

    # if everything is fine, we can cleanup the directory of the simulation

    rmtree(sim.path_run, ignore_errors=True)


@pytest.mark.slow
def test_SW_linear_base_from_SFD():

    params = params_SW()

    params.Ra_side = 1.86e8

    params.oper.enable_sfd = float(True)

    params.nek.general.end_time = 900
    params.nek.general.write_interval = 10

    aspect_ratio = 1.0
    nb_elements = 10
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)

    sim_sfd = Simul(params)

    sim_sfd.make.exec("run_fg", nproc=4)

    restart_file = sim_sfd.params.output.path_session / "cbox0.f00059"

    params = params_SW()

    params.Ra_side = 1.86e8

    nb_elements = 10
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)

    params.nek.general.start_from = "base_flow.restart"

    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"

    params.nek.general.extrapolation = "standard"

    sim = Simul(params)

    copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")

    sim.make.exec("run_fg", nproc=4)

    sim = load(sim.path_run)

    growth_rate = compute_growth_rate(sim)

    assert 0.0049 < growth_rate < 0.0055

    # if everything is fine, we can cleanup the directory of the simulations
    rmtree(sim_sfd.path_run, ignore_errors=True)
    rmtree(sim.path_run, ignore_errors=True)


@pytest.mark.slow
def test_SW_linear_base_provided():

    params = params_SW()

    restart_file = "./doc/examples/base_flow_side_simple.restart"

    params = params_SW()

    params.Ra_side = 1.86e8

    aspect_ratio = 1.0
    nb_elements = 10
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)

    params.nek.general.start_from = "base_flow.restart"

    params.nek.problemtype.equation = "incompLinNS"
    params.oper.elem.staggered = "auto"

    params.nek.general.extrapolation = "standard"

    sim = Simul(params)

    copyfile(restart_file, sim.params.output.path_session / "base_flow.restart")

    sim.make.exec("run_fg", nproc=4)

    growth_rate_linear = compute_growth_rate(sim)

    assert 0.0049 < growth_rate_linear < 0.0055

    # if everything is fine, we can cleanup the directory of the simulations
    rmtree(sim.path_run, ignore_errors=True)
