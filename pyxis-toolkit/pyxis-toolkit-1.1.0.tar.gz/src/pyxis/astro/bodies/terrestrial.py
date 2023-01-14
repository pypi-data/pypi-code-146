from math import cos, sin

from pyxis.astro.bodies.artificial import Spacecraft
from pyxis.astro.coordinates import AzElRange, ITRFstate, LLAstate
from pyxis.math.linalg import Matrix3D, Vector3D
from pyxis.time import Epoch


class GroundSite:
    def __init__(self, lla: LLAstate) -> None:
        """used for operations that require modeling of a terrestrial location

        :param lla: state that holds the latitude, longitude, and altitude of the ground station
        :type lla: LLAstate
        """
        self.lla: LLAstate = lla.copy()
        self.itrf_position: Vector3D = self.lla.itrf_position()
        slamb: float = sin(self.lla.longitude)
        clamb: float = cos(self.lla.longitude)
        spsi: float = sin(self.lla.latitude)
        cpsi: float = cos(self.lla.latitude)
        self.enz_matrix: Matrix3D = Matrix3D(
            Vector3D(-slamb, clamb, 0.0),
            Vector3D(-spsi * clamb, -spsi * slamb, cpsi),
            Vector3D(cpsi * clamb, cpsi * slamb, spsi),
        )

    @classmethod
    def from_itrf_position(cls, itrf: Vector3D) -> "GroundSite":
        """create a groundsite from cartesian coordinates

        :param itrf: earth-fixed position of the groundsite
        :type itrf: Vector3D
        :return: object stationed at the input earth-fixed vector
        :rtype: GroundSite
        """
        return cls(ITRFstate(Epoch(0), itrf, Vector3D(0, 0, 0)).lla_state())

    def enz_position(self, obj_itrf: Vector3D) -> Vector3D:
        """calculates the east-north-zenith coordinates of the argument position

        :param obj_itrf: itrf position of the object of interest
        :type obj_itrf: Vector3D
        :return: transformation of the argument itrf position to the east-north-zenith frame
        :rtype: Vector3D
        """
        return self.enz_matrix.multiply_vector(obj_itrf.minus(self.itrf_position))

    def angles_and_range(self, target: Spacecraft) -> AzElRange:
        """calculate the topo-centric angles and range to the argument spacecraft

        :param target: spacecraft being observed
        :type target: Spacecraft
        :return: azimuth, elevation, and range to the spacecraft from the ground site
        :rtype: AzElRange
        """
        return AzElRange.from_enz(self.enz_position(target.current_state().itrf_position()))
