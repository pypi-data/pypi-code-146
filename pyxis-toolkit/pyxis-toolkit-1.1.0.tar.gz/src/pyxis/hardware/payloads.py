from math import radians, tan

from pyxis.hardware.constraints import OpticalConstraints


class Camera:

    #: nominal full-length pixel count of a wide field-of-view camera assuming a square sensor
    DEFAULT_WIDE_PIXELS = 3072

    #: nominal full-length pixel count of a narrow field-of-view camera assuming a square sensor
    DEFAULT_NARROW_PIXELS = 3072

    #: nominal half-angle field-of-view in radians for a characterization-type camera
    DEFAULT_NFOV = radians(0.125)

    #: nominal half-angle field-of-view in radians for an observation-type camera
    DEFAULT_WFOV = radians(5)

    def __init__(self, pixels: float, fov: float) -> None:
        """class used to store sensor characteristics for optical observation hardware

        :param pixels: full-length pixel count assuming a square sensor
        :type pixels: float
        :param fov: half-angle field-of-view in radians
        :type fov: float
        """

        #: full-length pixel count assuming a square sensor
        self.pixels: float = pixels

        #: half-angle field-of-view in radians
        self.fov: float = fov

        #: constraints applied to the current camera
        self.limits: OpticalConstraints = OpticalConstraints(self.pixels, self.fov)

        #: scalar used to calculate the resolution at various ranges
        self.resolution_factor = 1 / self.pixels * 0.5

    @classmethod
    def wfov(cls) -> "Camera":
        """method used to instantiate a nominal wide field-of-view camera

        :return: camera containing wfov characteristics
        :rtype: Camera
        """
        return cls(Camera.DEFAULT_WIDE_PIXELS, Camera.DEFAULT_WFOV)

    @classmethod
    def nfov(cls) -> "Camera":
        """method used to instantiate a nominal narrow field-of-view camera

        :return: camera containing nfov characteristics
        :rtype: Camera
        """
        return cls(Camera.DEFAULT_NARROW_PIXELS, Camera.DEFAULT_NFOV)

    def resolution(self, r: float) -> float:
        """calculate the current resolution of the sensor for a given range

        :param r: range in km at which to calculate the resolution capability
        :type r: float
        :return: resolution in km
        :rtype: float
        """
        return tan(self.fov) * r * self.resolution_factor

    def range_error(self, r: float, d: float) -> float:
        """calculate the range estimation error at a given range when observing an object of the input diameter

        :param r: range in km that is being estimated
        :type r: float
        :param d: diameter in km of the object being observed
        :type d: float
        :return: error of the estimation in km
        :rtype: float
        """
        return self.resolution(r) / d * r

    def tracking_minimum(self, body_r: float) -> float:
        """calculate the minimum distance before the object being observed is too large to fit in the frame

        :param body_r: radius of the object being observed
        :type body_r: float
        :return: distance in km at which the fov will be filled
        :rtype: float
        """
        return body_r / tan(self.fov)
