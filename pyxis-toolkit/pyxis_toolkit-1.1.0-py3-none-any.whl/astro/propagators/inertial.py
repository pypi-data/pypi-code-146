from math import ceil, e, log
from typing import List

from pyxis.astro.coordinates import GCRFstate
from pyxis.math.constants import SEA_LEVEL_G, SECONDS_IN_DAY
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch


class RK4:

    #: Largest step to be taken by the integrator
    MAX_STEP = 300

    def __init__(self, state: GCRFstate) -> None:
        """class used to propagate a satellite state

        :param state: ECI state of the satellite to be propagated
        :type state: GCRFstate
        """
        #: the current state of the propagator
        self.state: GCRFstate = state.copy()

        #: integration step to be taken when the propagator is advanced
        self.step_size: float = RK4.MAX_STEP

        #: mass flow rate used to apply thrusts to propagator
        self.m_dot: float = 0

        #: initial mass when using the propagator to apply thrust
        self.m0: float = 0

        #: gcrf direction of any applied thrusts
        self.thrust_direction: Vector3D = Vector3D(0, 0, 0)

        #: specific impulse used to apply thrusts
        self.isp: float = 0

    def step(self) -> None:
        """advance the propagator state by the stored time step"""
        h = self.step_size

        epoch_0: Epoch = self.state.epoch.copy()

        self.state.thrust = self.thrust_vector(0)
        y: List[Vector3D] = self.state.vector_list()

        k1: List[Vector3D] = self.state.derivative()

        dsecs: float = h / 2
        ddays: float = dsecs / SECONDS_IN_DAY
        epoch_1 = epoch_0.plus_days(ddays)
        y1: GCRFstate = GCRFstate(epoch_1, y[0].plus(k1[0].scaled(dsecs)), y[1].plus(k1[1].scaled(dsecs)))
        y1.thrust = self.thrust_vector(dsecs)
        k2: List[Vector3D] = y1.derivative()

        y2: GCRFstate = GCRFstate(epoch_1, y[0].plus(k2[0].scaled(dsecs)), y[1].plus(k2[1].scaled(dsecs)))
        y2.thrust = self.thrust_vector(dsecs)
        k3: List[Vector3D] = y2.derivative()

        epoch_2 = epoch_1.plus_days(ddays)
        y3: GCRFstate = GCRFstate(epoch_2, y[0].plus(k3[0].scaled(h)), y[1].plus(k3[1].scaled(h)))
        y3.thrust = self.thrust_vector(dsecs * 2)
        k4: List[Vector3D] = y3.derivative()

        coeff: float = 1 / 6
        dv: Vector3D = k1[0].plus(k2[0].scaled(2).plus(k3[0].scaled(2).plus(k4[0]))).scaled(coeff)
        da: Vector3D = k1[1].plus(k2[1].scaled(2).plus(k3[1].scaled(2).plus(k4[1]))).scaled(coeff)

        self.state = GCRFstate(
            epoch_2,
            self.state.position.plus(dv.scaled(h)),
            self.state.velocity.plus(da.scaled(h)),
        )

    def maneuver(self, gcrf_thrust: Vector3D, m_dot: float, m0: float, isp: float) -> None:
        """propagate the state using continuous thrust principles

        :param gcrf_thrust: components of the maneuver in the gcrf frame
        :type gcrf_thrust: Vector3D
        :param m_dot: mass flow rate
        :type m_dot: float
        :param m0: initial mass
        :type m0: float
        :param isp: specific impulse
        :type isp: float
        """
        m_spec: float = m_dot / m0
        dv_duration: float = (1 / m_spec) * (
            1 - e ** (m_spec * gcrf_thrust.magnitude() / (-isp * m_spec * SEA_LEVEL_G))
        )
        self.thrust_direction = gcrf_thrust.copy()
        self.m0 = m0
        self.m_dot = m_dot
        self.isp = isp
        self.step_to_epoch(self.state.epoch.plus_days(dv_duration / SECONDS_IN_DAY))
        self.m0 = 0
        self.m_dot = 0

    def step_to_epoch(self, epoch: Epoch) -> None:
        """advance the propagator state to the argument epoch

        :param epoch: time of state to be calculated
        :type epoch: Epoch
        """

        # Calculate time delta in seconds
        dt = (epoch.value - self.state.epoch.value) * SECONDS_IN_DAY

        # Determine number of steps required to meet new epoch while staying below the maximum step
        num_steps = ceil(abs(dt / self.MAX_STEP))

        # Store current step size
        old_step = self.step_size

        # Temporarily set step size to calculated dt
        if num_steps > 0:
            self.step_size = dt / num_steps

        # Step until desired epoch is achieved
        step_n = 0
        while step_n < num_steps:
            self.step()
            step_n += 1

        # Reset step size
        self.step_size = old_step

    def thrust_vector(self, dt: float) -> Vector3D:
        """calculate the acceleration vector due to thrust

        :param dt: time step at which to calculate the thrust
        :type dt: float
        :return: thrust vector with gcrf components
        :rtype: Vector3D
        """
        a: Vector3D = Vector3D(0, 0, 0)
        if self.m_dot != 0:
            if dt == 0:
                a = self.thrust_direction.normalized().scaled(self.m_dot * self.isp * SEA_LEVEL_G / self.m0)
            else:
                ln = log(1 - self.m_dot * dt / self.m0)
                mt = self.m0 - self.m_dot * dt
                f = self.m_dot * self.isp * SEA_LEVEL_G
                dv: Vector3D = self.thrust_direction.normalized().scaled((-f / self.m_dot) * ln)
                a = dv.scaled((self.m_dot / mt) * (1 / (-log(1 - self.m_dot * dt / self.m0))))

        return a
