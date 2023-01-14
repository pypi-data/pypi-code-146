from math import cos, e, log10, pi, radians, sin
from typing import List

from pyxis.astro.bodies.celestial import Earth
from pyxis.astro.coordinates import GCRFstate, HillState
from pyxis.astro.propagators.inertial import RK4
from pyxis.astro.propagators.relative import Hill
from pyxis.estimation.filtering import RelativeKalman
from pyxis.estimation.obs import SpaceObservation
from pyxis.hardware.payloads import Camera
from pyxis.math.constants import SEA_LEVEL_G, SECONDS_IN_DAY
from pyxis.math.linalg import Vector3D
from pyxis.time import Epoch


class Spacecraft:

    #: The default body radius of the satellite (km)
    DEFAULT_RADIUS: float = 0.005

    #: The default albedo of the satellite used for optical modeling (unitless)
    DEFAULT_ALBEDO: float = 0.3

    #: Available control methods of the vehicle's attitude (lvlh == z to earth, solar == -z to sun, target == z to rso)
    STEERING_MODES: List[str] = ["lvlh", "solar", "target"]

    #: Default scalar to use with calculating slew times (1/(radians per day))
    DEFAULT_SLEW_SCALE: float = 1 / (radians(0.5) * SECONDS_IN_DAY)

    #: Default tolerance to use for statistical attitude modeling (radians)
    DEFAULT_POINTING_ACCURACY: float = 1e-5

    #: Default dry mass of the spacecraft at launch (kg)
    DEFAULT_MASS: float = 600

    #: Default propellant mass of the spacecraft at launch (kg)
    DEFAULT_PROP_MASS: float = 200

    #: Default mass flow rate used to calculate thrust
    DEFAULT_M_DOT: float = 0.003

    #: Default specific impulse of the propellant used to calculate thrust
    DEFAULT_ISP: float = 350

    def __init__(self, state: GCRFstate) -> None:
        """class used to model the behaviors of man-made satellites

        :param state: starting inertial state of the satellite
        :type state: GCRFstate
        """

        #: Used to retain knowledge of the state when the satellite was first created
        self.initial_state: GCRFstate = state.copy()

        #: Used to solve the state of the spacecraft at various times in the orbit
        self.propagator: RK4 = RK4(self.initial_state)

        #: Used for optical modeling of the satellite
        self.albedo: float = Spacecraft.DEFAULT_ALBEDO

        #: Used for various physical modeling methods of the satellite
        self.body_radius: float = Spacecraft.DEFAULT_RADIUS

        #: Payload used for metric observation and close-proximity tracking
        self.wfov: Camera = Camera.wfov()

        #: Payload used for distant tracking and characterization
        self.nfov: Camera = Camera.nfov()

        #: Used for state estimation when target-tracking
        self.filter: RelativeKalman

        #: Used to store the current steering mode of the satellite
        self.steering: str = Spacecraft.STEERING_MODES[0]

        #: The target satellite when the calling spacecraft is in target-tracking mode
        self.tracked_target: Spacecraft

        #: Indicates whether the spacecraft is in a stable attitude mode or in a transitioning slew
        self.slewing: bool = False

        #: Epoch used to indicate when self.slewing can be switched to 'False'
        self.slew_stop: Epoch

        #: Used to calculate slew times
        self.slew_scalar: float = Spacecraft.DEFAULT_SLEW_SCALE

        #: Used to apply noise to attitude vectors
        self.pointing_accuracy = Spacecraft.DEFAULT_POINTING_ACCURACY

        #: Mass flow rate used to perform finite maneuvers
        self.m_dot = Spacecraft.DEFAULT_M_DOT

        #: specific impulse used to perform finite maneuvers
        self.isp = Spacecraft.DEFAULT_ISP

        #: Mass of the spacecraft without propellant included
        self.dry_mass = Spacecraft.DEFAULT_MASS

        #: Mass of the propellant on the spacecraft
        self.propellant_mass = Spacecraft.DEFAULT_PROP_MASS

        self.update_attitude()

    def total_mass(self) -> float:
        """calculates the mass of the bus plus propellant

        :return: wet mass of the spacecraft (kg)
        :rtype: float
        """
        return self.dry_mass + self.propellant_mass

    def impulsive_maneuver(self, ric_burn: Vector3D) -> None:
        """applies a velocity change to the current state to model an instant maneuver

        :param ric_burn: burn vector with components of radial, in-track, and cross-track (km/s)
        :type ric_burn: Vector3D
        """
        self.propagator = RK4(GCRFstate.from_hill(self.current_state(), HillState(Vector3D(0, 0, 0), ric_burn)))

    def finite_maneuver(self, ric_dv: Vector3D) -> None:
        """perform a maneuver using ric acceleration accross a specified time

        :param ric_dv: maneuver in the radial, in-track, and cross-track components (km/s)
        :type ric_dv: Vector3D
        :param dt: duration of the maneuver in days
        :type dt: float
        """
        gcrf_thrust: Vector3D = HillState.frame_matrix(self.current_state()).multiply_vector(ric_dv)
        self.propagator.maneuver(
            gcrf_thrust,
            self.m_dot,
            self.total_mass(),
            self.isp,
        )
        m_spec: float = self.m_dot / self.total_mass()
        dt: float = (-1 / m_spec) * (1 - e ** (m_spec * gcrf_thrust.magnitude() / (-self.isp * m_spec * SEA_LEVEL_G)))
        self.propellant_mass -= self.m_dot * dt

    def sma(self) -> float:
        """calculate the semi-major axis of the calling spacecraft

        :return: the spacecraft's semi-major axis in km
        :rtype: float
        """
        r = self.position().magnitude()
        v = self.velocity().magnitude()
        return 1 / (2 / r - v * v / Earth.MU)

    def acquire(self, seed: "Spacecraft") -> None:
        """initialize the kalman filter and begin tracking the argument satellite

        :param seed: the estimated state of the satellite to be tracked
        :type seed: Spacecraft
        """

        self.filter = RelativeKalman(
            self.current_epoch(),
            Hill(
                HillState.from_gcrf(seed.current_state(), self.current_state()),
                self.sma(),
            ),
        )
        self.track_state(seed)

    def observe_wfov(self, target: "Spacecraft") -> SpaceObservation:
        """produce a simulated observation from the wfov

        :param target: satellite to be observed
        :type target: Spacecraft
        :return: simulated observation
        :rtype: SpaceObservation
        """
        truth_vector: Vector3D = self.target_vector(target)
        truth_range: float = truth_vector.magnitude()
        range_error: float = self.wfov.range_error(truth_range, target.body_radius * 2)
        return SpaceObservation(
            self.current_state(),
            truth_vector.with_noise(range_error, self.pointing_accuracy),
            range_error,
            self.pointing_accuracy,
        )

    def observe_nfov(self, target: "Spacecraft") -> SpaceObservation:
        """produce a simulated observation from the nfov

        :param target: satellite to be observed
        :type target: Spacecraft
        :return: simulated observation
        :rtype: SpaceObservation
        """
        truth_vector: Vector3D = self.target_vector(target)
        truth_range: float = truth_vector.magnitude()
        range_error: float = self.nfov.range_error(truth_range, target.body_radius * 2)
        return SpaceObservation(
            self.current_state(),
            truth_vector.with_noise(range_error, self.pointing_accuracy),
            range_error,
            self.pointing_accuracy,
        )

    def process_wfov(self, target: "Spacecraft") -> None:
        """create a simulated observation of the argument spacecraft and feed the ob into the kalman filter

        :param target: satellite to be observed
        :type target: Spacecraft
        """
        ob = self.observe_wfov(target)
        self.filter.process(ob)

    def process_nfov(self, target: "Spacecraft") -> None:
        """create a simulated observation of the argument spacecraft and feed the ob into the kalman filter

        :param target: satellite to be observed
        :type target: Spacecraft
        """
        ob = self.observe_nfov(target)
        self.filter.process(ob)

    def update_attitude(self) -> None:
        """calculate and store the appropriate body axis values depending on steering mode"""
        if self.steering == Spacecraft.STEERING_MODES[0]:

            # Point payload deck at Earth
            self.body_z = self.earth_vector()

            # Align solar panels with orbit normal
            self.body_y = self.position().cross(self.velocity())

            # Complete right-hand rule
            self.body_x = self.body_y.cross(self.body_z)

        elif self.steering == Spacecraft.STEERING_MODES[1]:

            # Point payload deck away from Sun
            self.body_z = self.sun_vector().scaled(-1)

            # Create arbitrary x
            self.body_x = self.body_z.cross(Vector3D(0, 0, 1))

            # Complete right-hand rule
            self.body_y = self.body_z.cross(self.body_x)

        elif self.steering == Spacecraft.STEERING_MODES[2]:

            # Step the tracked spacecraft if epochs are not in sync
            if self.tracked_target.current_epoch().value != self.current_epoch().value:
                self.tracked_target.step_to_epoch(self.current_epoch())

            # Point payload deck at target
            self.body_z = self.target_vector(self.tracked_target)

            # Align solar panels
            self.body_y = self.body_z.cross(self.sun_vector())

            # Complete right-hand rule
            self.body_x = self.body_y.cross(self.body_z)

        if self.slewing:
            if self.current_epoch().value > self.slew_stop.value:
                self.slewing = False

    def track_lvlh(self) -> None:
        """store attitude with payload toward earth and panels along orbit normal"""
        # Include slew duration if not already in lvlh
        if self.steering != Spacecraft.STEERING_MODES[0]:
            self.steering = Spacecraft.STEERING_MODES[0]
            self.slewing = True
            t: float = self.body_z.angle(self.position().scaled(-1)) * self.slew_scalar
            self.slew_stop = self.current_epoch().plus_days(t)

        self.update_attitude()

    def track_sun(self) -> None:
        """store attitude with payload opposite to Sun"""
        # Include slew duration if not already sun-pointing
        if self.steering != Spacecraft.STEERING_MODES[1]:
            self.steering = Spacecraft.STEERING_MODES[1]
            self.slewing = True
            t: float = self.body_z.angle(self.sun_vector().scaled(-1)) * self.slew_scalar
            self.slew_stop = self.current_epoch().plus_days(t)

        self.update_attitude()

    def track_state(self, target: "Spacecraft") -> None:
        """store attitude with payload toward target

        :param target: spacecraft to be tracked
        :type target: Spacecraft
        """
        # Include slew duration if not already target-pointing
        if self.steering != Spacecraft.STEERING_MODES[2]:
            self.steering = Spacecraft.STEERING_MODES[2]
            self.tracked_target = target
            self.slewing = True
            t: float = self.body_z.angle(self.target_vector(target)) * self.slew_scalar
            self.slew_stop = self.current_epoch().plus_days(t)

        self.update_attitude()

    def velocity(self) -> Vector3D:
        """retrieve current ECI velocity vector

        :return: velocity vector as determined by the satellite's propagator
        :rtype: Vector3D
        """
        return self.propagator.state.velocity.copy()

    def detect(self, target: "Spacecraft") -> bool:
        """determine if a satellite can be detected given payload constraints

        :param target: satellite to be detected
        :type target: Spacecraft
        :return: status of detection
        :rtype: bool
        """
        success: bool = True
        if self.sun_angle(target) < self.wfov.limits.sun_soft:
            success = False
        elif self.earth_angle(target) < self.wfov.limits.earth:
            success = False
        elif self.moon_angle(target) < self.wfov.limits.moon:
            success = False
        elif self.visual_magnitude(target) > self.wfov.limits.vismag:
            success = False
        elif self.body_z.angle(self.target_vector(target)) > self.wfov.limits.bore:
            success = False
        return success

    def visual_magnitude(self, target: "Spacecraft") -> float:
        """calculate the visual magnitude of a satellite

        :param target: satellite being observed
        :type target: Spacecraft
        :return: visual magnitude of the observed spacecraft
        :rtype: float
        """
        # Store the target's body radius
        r: float = self.body_radius

        # Calculate the range to the target
        dist: float = self.range(target)

        # Calculate the sun angle
        phi: float = pi - self.sun_angle(target)

        # Calculate the flux and vismag
        fdiff: float = (2 / 3) * self.albedo * r * r / (pi * dist * dist) * ((sin(phi) + (pi - phi) * cos(phi)))
        return -26.74 - 2.5 * log10(fdiff)

    def sun_angle(self, target: "Spacecraft") -> float:
        """calculate the angle between the sun and target using the calling spacecraft as the vertex

        :param target: satellite being observed
        :type target: Spacecraft
        :return: angle between target and sun vector in radians
        :rtype: float
        """
        return self.sun_vector().angle(self.target_vector(target))

    def moon_angle(self, target: "Spacecraft") -> float:
        """calculate the angle between the moon and target using the calling spacecraft as the vertex

        :param target: satellite being observed
        :type target: Spacecraft
        :return: angle between target and moon vector in radians
        :rtype: float
        """
        return self.moon_vector().angle(self.target_vector(target))

    def earth_angle(self, target: "Spacecraft") -> float:
        """calculate the angle between the earth and target using the calling spacecraft as the vertex

        :param target: satellite being observed
        :type target: Spacecraft
        :return: angle between target and earth vector in radians
        :rtype: float
        """
        return self.earth_vector().angle(self.target_vector(target))

    def range(self, target: "Spacecraft") -> float:
        """calculate the distance from the calling spacecraft to the argument spacecraft

        :param target: spacecraft representing the range vector's head
        :type target: Spacecraft
        :return: distance to the argument spacecraft in km
        :rtype: float
        """
        return self.target_vector(target).magnitude()

    def position(self) -> Vector3D:
        """retrieve the spacecraft's current ECI position vector

        :return: spacecraft's current position vector as determined by the propagator
        :rtype: Vector3D
        """
        return self.current_state().position.copy()

    def step(self) -> None:
        """solve the vehicle's position and velocity at the next time step"""
        self.propagator.step()
        self.update_attitude()

    def step_to_epoch(self, epoch: Epoch) -> None:
        """solve the vehicle's position and velocity at the argument epoch

        :param epoch: desired time at which the vehicle's state should be solved
        :type epoch: Epoch
        """
        self.propagator.step_to_epoch(epoch)
        self.update_attitude()

    def sun_vector(self) -> Vector3D:
        """calculate the ECI vector from the vehicle to the sun

        :return: vector originating at self and terminating at the sun
        :rtype: Vector3D
        """
        return self.current_state().sun_vector()

    def moon_vector(self) -> Vector3D:
        """calculate the ECI vector from the vehicle to the moon

        :return: vector originating at self and terminating at the moon
        :rtype: Vector3D
        """
        return self.current_state().moon_vector()

    def earth_vector(self) -> Vector3D:
        """calculate the ECI vector from the vehicle to the earth

        :return: vector originating at self and terminating at the earth
        :rtype: Vector3D
        """
        return self.position().scaled(-1)

    def target_vector(self, target: "Spacecraft") -> Vector3D:
        """calculate the ECI vector from the vehicle to the argument spacecraft

        :param target: spacecraft acting as the vector head
        :type target: Spacecraft
        :return: vector originating at self and terminating at the target's position
        :rtype: Vector3D
        """
        return target.position().minus(self.position())

    def hill_position(self, target: "Spacecraft") -> Vector3D:
        """calculate the hill position vector from self to the argument spacecraft

        :param target: vehicle acting as the relative position vector head
        :type target: Spacecraft
        :return: vector originating at self and terminating at the target's position in the hill frame
        :rtype: Vector3D
        """
        return HillState.from_gcrf(target.current_state(), self.current_state()).position

    def current_state(self) -> "GCRFstate":
        """retrieve the vehicle's current ECI state

        :return: current ECI state as determined by the propagator
        :rtype: GCRFstate
        """
        return self.propagator.state.copy()

    def current_epoch(self) -> Epoch:
        """retrieve the vehicle's current time

        :return: epoch of the vehicle as determined by the propagator
        :rtype: Epoch
        """
        return self.current_state().epoch.copy()
