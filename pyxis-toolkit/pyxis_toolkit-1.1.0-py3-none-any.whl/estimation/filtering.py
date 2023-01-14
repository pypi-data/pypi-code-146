from pyxis.astro.coordinates import GCRFstate, HillState, SphericalPosition
from pyxis.astro.propagators.relative import Hill
from pyxis.estimation.obs import SpaceObservation
from pyxis.math.constants import SECONDS_IN_DAY
from pyxis.math.linalg import Matrix3by6, Matrix3D, Matrix6by3, Matrix6D, Vector3D, Vector6D
from pyxis.time import Epoch


class RelativeKalman:

    #: Covariance matrix to be used when the filter is initialized (km and km/s)
    DEFAULT_COVARIANCE = Matrix6D(
        Vector6D(0.5, 0, 0, 0, 0, 0),
        Vector6D(0, 0.5, 0, 0, 0, 0),
        Vector6D(0, 0, 0.5, 0, 0, 0),
        Vector6D(0, 0, 0, 5e-5, 0, 0),
        Vector6D(0, 0, 0, 0, 5e-5, 0),
        Vector6D(0, 0, 0, 0, 0, 5e-5),
    )

    #: Processing noise of the system
    DEFAULT_NOISE = Matrix6D(
        Vector6D(1e-16, 0, 0, 0, 0, 0),
        Vector6D(0, 1e-16, 0, 0, 0, 0),
        Vector6D(0, 0, 1e-16, 0, 0, 0),
        Vector6D(0, 0, 0, 1e-16, 0, 0),
        Vector6D(0, 0, 0, 0, 1e-16, 0),
        Vector6D(0, 0, 0, 0, 0, 1e-16),
    )

    #: Observation matrix of a position-only system
    H: Matrix3by6 = Matrix3by6(
        Vector6D(1, 0, 0, 0, 0, 0),
        Vector6D(0, 1, 0, 0, 0, 0),
        Vector6D(0, 0, 1, 0, 0, 0),
    )

    #: Transposed H
    HT: Matrix6by3 = H.transpose()

    #: Matrix with a diagonal of all 1 and off-diagonal of 0
    I: Matrix6D = Matrix6D.identity()

    def __init__(self, epoch: Epoch, propagator: Hill) -> None:
        """class used to act as the navigation filter for a position-only measurement source

        :param epoch: time filter is to be initialized
        :type epoch: Epoch
        :param propagator: estimated Hill state of the spacecraft being observed
        :type propagator: Hill
        """
        #: current time of the filter state
        self.epoch: Epoch = epoch.copy()

        #: propagator used to estimate the relative state of the observed spacecraft
        self.propagator: Hill = propagator

        #: current state of the filter
        self.x00: Vector6D = self.propagator.state.vector.copy()

        #: predicted state of the filter
        self.x10: Vector6D

        #: current covariance of the state
        self.p00: Matrix6D = RelativeKalman.DEFAULT_COVARIANCE

        #: predicted covariance of the state
        self.p10: Matrix6D

        #: processing noise of the filter
        self.q: Matrix6D = RelativeKalman.DEFAULT_NOISE

        #: state transition matrix for the filter state
        self.f: Matrix6D = self.propagator.system_matrix(0)

        #: gain of the filter
        self.k: Matrix6by3

        #: current measurement
        self.z: Vector3D

        #: error in km of the current measurement
        self.range_error: float = 0

        #: error in radians of the current measurement
        self.angular_error: float = 0

        #: measurement uncertainty matrix
        self.r: Matrix3D

    def predict_covariance(self) -> None:
        """calculate the next covariance"""
        self.p10 = self.f.multiply_matrix(self.p00.multiply_matrix(self.f.transpose())).plus(self.q)

    def gain(self) -> None:
        """calculate the gain of the system"""
        hph: Matrix3D = self.H.multiply_matrix_6by3(self.p10.multiply_matrix_6by3(self.HT))
        self.k = self.p10.multiply_matrix_6by3(self.HT.multiply(hph.plus(self.r).inverse()))

    def predict_state(self, dt: float) -> None:
        """calculate the expected future state of the system

        :param dt: number of seconds between current observation and previous observation
        :type dt: float
        """
        self.f = self.propagator.system_matrix(dt)
        self.x10 = self.f.multiply_vector(self.x00)

    def update_state(self) -> None:
        """correct predicted state and store as current state"""
        self.x00 = self.x10.plus(self.k.multiply_vector(self.z.minus(self.H.multiply_vector(self.x10))))
        self.propagator.state = HillState.from_state_vector(self.x00)

    def update_covariance(self) -> None:
        """correct predicted covariance and store as current covariance"""
        m1: Matrix6D = self.I.minus(self.k.multiply_matrix3by6(self.H))
        m2: Matrix6D = self.k.multiply_matrix3by6(self.r.multiply_matrix3by6(self.k.transpose()))
        self.p00 = m1.multiply_matrix(self.p10.multiply_matrix(m1.transpose())).plus(m2)

    def predict(self, dt: float) -> None:
        """calculate predicted state and covariance"""
        self.predict_state(dt)
        self.predict_covariance()

    def update(self) -> None:
        """correct predicted state and covariance"""
        self.gain()
        self.update_state()
        self.update_covariance()

    def process(self, ob: SpaceObservation) -> None:
        """include a new observation into the current estimation

        :param ob: observation to be added into the system
        :type ob: SpaceObservation
        """
        dt: float = (ob.observer_state.epoch.value - self.epoch.value) * SECONDS_IN_DAY
        self.epoch = ob.observer_state.epoch.copy()
        gcrf_ob: GCRFstate = GCRFstate(
            self.epoch, ob.observer_state.position.plus(ob.observed_direction), ob.observer_state.velocity
        )
        self.z = HillState.from_gcrf(gcrf_ob, ob.observer_state).position

        spherical_ob = SphericalPosition(
            ob.range + ob.range_error, ob.right_ascension + ob.angular_error, ob.declination + ob.angular_error
        )
        errors: Vector3D = spherical_ob.to_cartesian().minus(ob.observed_direction)
        gcrf_errors: GCRFstate = GCRFstate(
            self.epoch, ob.observer_state.position.plus(errors), ob.observer_state.velocity
        )
        hill_errors: Vector3D = HillState.from_gcrf(gcrf_errors, ob.observer_state).position
        self.r = Matrix3D(
            Vector3D(
                hill_errors.x * hill_errors.x,
                0,
                0,
            ),
            Vector3D(
                0,
                hill_errors.y * hill_errors.y,
                0,
            ),
            Vector3D(
                0,
                0,
                hill_errors.z * hill_errors.z,
            ),
        )
        self.range_error = ob.range_error
        self.angular_error = ob.angular_error
        self.predict(dt)
        self.update()
