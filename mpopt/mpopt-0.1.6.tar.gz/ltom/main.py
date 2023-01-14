"""
Created: July 2020
Author : Vaibhav Gupta
"""
import numpy as np
import matplotlib.pyplot as plt
from casadi import *

import sys
from context import mpopt
from mpopt import mp

from track import Track
import plotter

# N_SEGMENTS = 64

NX_MODEL = 4
NX = NX_MODEL + 3
NU = 2

LF = 1.4
LR = 1.6

TRACK = Track()


def car_dynamics(x, u, t):
    # States and inputs
    X = x[0]
    Y = x[1]
    theta = x[2]
    delta = x[3]

    v = u[0]
    delta_dot = u[1]

    beta = atan2(LR * tan(delta), LF + LR)
    vx = v * cos(beta)
    vy = v * sin(beta)

    return (
        [
            v * cos(theta + beta),
            v * sin(theta + beta),
            (v * cos(beta) * tan(delta)) / (LF + LR),
            delta_dot,
        ],
        vx,
        vy,
    )


def dynamics(x, u, t, a):
    s = x[NX_MODEL + 1]
    td = x[NX_MODEL + 2]

    car_dyn, vx, vy = car_dynamics(x[:NX_MODEL], u[:2], t)
    Td, theta, curv = TRACK.get_track(s)

    alpha = x[2] - theta

    s_dot = (vx * cos(alpha) - vy * sin(alpha)) / (1 - td * curv)
    d_dot = vx * sin(alpha) + vy * cos(alpha)

    return [
        a[0] * temp
        for temp in [
            *car_dyn,
            1,
            s_dot,
            d_dot,
        ]
    ]


def running_cost(x, u, t, a):
    # s = x[NX_MODEL + 1]
    # td = x[NX_MODEL + 2]
    #
    # car_dyn, vx, vy = car_dynamics(x[:NX_MODEL], u[:2], t)
    # Td, theta, curv = TRACK.get_track(s)
    #
    # alpha = x[2] - theta
    # s_dot = (vx * cos(alpha) - vy * sin(alpha)) / (1 - td * curv)

    return u[0] * u[0] + u[1] * u[1]


def path_constraints(x, u, t, a):
    s = x[NX_MODEL + 1]
    td = x[NX_MODEL + 2]

    car_dyn, vx, vy = car_dynamics(x[:NX_MODEL], u[:2], t)
    Td, theta, curv = TRACK.get_track(s)

    alpha = x[2] - theta
    s_dot = (vx * cos(alpha) - vy * sin(alpha)) / (1 - td * curv)

    return [
        td ** 2 - Td ** 2,
        -s_dot,
    ]


def terminal_constraints(xf, tf, x0, t0, a):
    s = xf[NX_MODEL + 1]
    s_T = TRACK.goal
    e = s_T - s
    return [e]


def terminal_costs(xf, tf, x0, t0, a):
    return a[0] ** 2


if __name__ == "__main__":
    ocp = mp.OCP(n_states=NX, n_controls=NU, n_params=1)
    ocp.dynamics[0] = dynamics
    # ocp.running_costs[0] = running_cost
    ocp.terminal_costs[0] = terminal_costs
    ocp.path_constraints[0] = path_constraints
    ocp.terminal_constraints[0] = terminal_constraints
    ocp.x00[0] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    ocp.lbx[0] = [-np.inf, -np.inf, -np.inf, -np.pi / 4, 0, 0, -np.inf]
    ocp.ubx[0] = [np.inf, np.inf, np.inf, np.pi / 4, np.inf, np.inf, np.inf]
    ocp.lbu[0] = [-10, -10]
    ocp.ubu[0] = [10, 10]
    ocp.tf0[0] = 1.0
    ocp.lbtf[0] = 1.0
    ocp.ubtf[0] = 1.0
    ocp.lba[0] = 30
    ocp.uba[0] = 300
    ocp.u00[0] = [10, 0]
    # ocp.diff_u[0] = 1
    # ocp.lbdu[0] = -1
    # ocp.ubdu[0] = 1
    # ocp.midu[0] = 1
    # ocp.du_continuity[0] = 1
    ocp.validate()
    order = 30
    segs = 1

    opt = mp.mpopt(ocp, n_segments=segs, poly_orders=order, scheme="CGL")
    # opt = mp.mpopt_h_adaptive(ocp, n_segments=segs, poly_orders=order, scheme="CGL")
    # opt = mp.mpopt_adaptive(ocp, n_segments=segs, poly_orders=order, scheme="LGR")
    sol = opt.solve(
        max_iter=5,
        mpopt_options={"method": "residual", "sub_method": "equal_area"},
        # nlp_options={"ipopt.acceptable_tol": 1e-10,}
        # max_iter=3,
        # mpopt_options={"method": "control_slope", "sub_method": "equal_area"},
    )

    mp.post_process._INTERPOLATION_NODES_PER_SEG = 100

    post = opt.process_results(sol, plot=True)
    x, u, t, a = post.get_data(0, interpolate=True)

    plt.figure("Open Loop")
    plotter.drawTrack(TRACK.track)
    plotter.drawPlot(
        x[:, 0],
        x[:, 1],
        x[:, 2],
        # t=x[:, -3],
        with_arrow=False,
        title="Open Loop",
        order=order,
    )
    plt.ylabel("Y [$m$]")
    plt.xlabel("X [$m$]")
    plt.axis("equal")
    plt.tight_layout()

    # Should be constant
    # plt.figure("Tuning Parameter")
    # plt.plot(a)
    # plt.ylabel("Tuning Parameter")
    print("Time =", a)

    post.plot_u()
    # # Control
    # plt.figure("Control")
    # plt.plot(u[:, 0:2])
    # plt.ylabel("Control")
    plt.show()
