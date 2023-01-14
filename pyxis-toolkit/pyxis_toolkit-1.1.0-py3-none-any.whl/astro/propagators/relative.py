from math import cos, sin, sqrt

from pyxis.astro.bodies.celestial import Earth
from pyxis.astro.coordinates import HillState
from pyxis.math.linalg import Matrix6D, Vector6D


class Hill:

    #: Nominal time to advance the propagator in seconds when no dt is given
    DEFAULT_STEP_SIZE: float = 600

    def __init__(self, state: HillState, sma: float) -> None:
        """class used to calculate the relative position of a spacecraft using Hill's equations

        :param state: relative state of the satellite to be propagated
        :type state: HillState
        :param sma: semi-major axis of the origin vehicle in km
        :type sma: float
        """
        #: current state of the propagator
        self.state: HillState = state.copy()

        #: semi-major axis of the origin spacecraft
        self.sma: float = sma

        #: orbital rate of the system
        self.n: float = sqrt(Earth.MU / (sma * sma * sma))

        #: step in seconds used to advance the propagator
        self.step_size = Hill.DEFAULT_STEP_SIZE

    def system_matrix(self, t: float) -> Matrix6D:
        """return the system matrix required to advance the initial state by the input t

        :param t: number of seconds between initial state and desired state
        :type t: float
        :return: system matrix used to advance the propagator
        :rtype: Matrix6D
        """
        n = self.n
        n_inv = 1 / n
        sn = sin(n * t)
        cs = cos(n * t)

        # define system matrix of x, y, z, x_dot, y_dot, z_dot equations
        sys_mat = Matrix6D(
            Vector6D(4 - 3 * cs, 0, 0, sn * n_inv, 2 * (1 - cs) * n_inv, 0),
            Vector6D(
                6 * (sn - n * t),
                1,
                0,
                -2 * (1 - cs) * n_inv,
                (4 * sn - 3 * n * t) * n_inv,
                0,
            ),
            Vector6D(0, 0, cs, 0, 0, sn * n_inv),
            Vector6D(3 * n * sn, 0, 0, cs, 2 * sn, 0),
            Vector6D(-6 * n * (1 - cs), 0, 0, -2 * sn, 4 * cs - 3, 0),
            Vector6D(0, 0, -n * sn, 0, 0, cs),
        )

        return sys_mat

    def step_by_seconds(self, t: float) -> None:
        """advance the propagator by a variable time

        :param t: number of seconds to advance the propagator
        :type t: float
        """
        self.state = HillState.from_state_vector(self.system_matrix(t).multiply_vector(self.state.vector))

    def step(self) -> None:
        """advance the propagator by one time step"""
        self.step_by_seconds(self.step_size)
