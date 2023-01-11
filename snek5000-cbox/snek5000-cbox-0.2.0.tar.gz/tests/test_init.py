from shutil import rmtree

import numpy as np

from snek5000_cbox.solver import Simul
from snek5000 import load


def test_simple_simul():

    params = Simul.create_default_params()

    aspect_ratio = 1.0
    params.prandtl = 0.71

    # for aspect ratio 1, Ra_c = 1.825E08
    params.Ra_side = 1.83e08

    params.output.sub_directory = "tests_snek_cbox"

    params.oper.nproc_min = 2
    params.oper.dim = 2

    nb_elements = 8
    params.oper.ny = nb_elements
    params.oper.nx = int(nb_elements / aspect_ratio)

    Ly = params.oper.Ly
    Lx = params.oper.Lx = Ly / aspect_ratio

    params.oper.elem.order = params.oper.elem.order_out = 7

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

    params.nek.general.num_steps = 5000
    params.nek.general.write_interval = 500

    params.nek.general.variable_dt = False
    params.nek.general.dt = 0.05
    params.nek.general.time_stepper = "BDF3"
    params.nek.general.extrapolation = "OIFS"

    params.output.phys_fields.write_interval_pert_field = 500
    params.output.history_points.write_interval = 10

    sim = Simul(params)

    sim.make.list()

    # if everything is fine, we can cleanup the directory of the simulation
    rmtree(sim.path_run, ignore_errors=True)


def test_init_side():

    params = Simul.create_default_params()

    params.oper.dim = 2
    params.Ra_side = 1.0

    Simul(params)

    params.oper.y_periodicity = True

    Simul(params)

    params.oper.y_periodicity = False
    params.oper.dim = 3

    Simul(params)

    params.oper.z_periodicity = True

    Simul(params)

    params.oper.y_periodicity = True

    Simul(params)

    params.oper.enable_sfd = float(True)

    Simul(params)


def test_init_RB():

    params = Simul.create_default_params()

    params.oper.dim = 2
    params.Ra_vert = 1.0

    Simul(params)

    params.oper.x_periodicity = True

    Simul(params)

    params.oper.x_periodicity = False
    params.oper.dim = 3

    Simul(params)

    params.oper.z_periodicity = True

    Simul(params)

    params.oper.x_periodicity = True

    Simul(params)


def test_init_mix():

    params = Simul.create_default_params()

    params.oper.dim = 2
    params.Ra_side = 1.0
    params.Ra_vert = 1.0

    Simul(params)

    params.oper.dim = 3

    Simul(params)

    params.oper.z_periodicity = True

    Simul(params)
