from math import radians, tan


class OpticalConstraints:

    #: nominal angle at which sensor damage will occur (radians)
    DEFAULT_SUN_HARD = radians(60)

    #: nominal sun angle at which an object can be observed (radians)
    DEFAULT_SUN_SOFT = radians(90)

    #: nominal moon angle at which an object can be observed (radians)
    DEFAULT_MOON_LIMIT = radians(10)

    #: nominal earth angle at which an object can be observed (radians)
    DEFAULT_EARTH_LIMIT = radians(20)

    #: visual magnitude require before an object is considered detected
    DEFAULT_LIMITING_MAG = 15

    #: nominal resolution required for a successful characterization (km)
    DEFAULT_RESOLUTION_LIMIT = 1e-5

    #: nominal ratio of FOV an object can be off center for detection to occur (must be > 0 and <= 1)
    DEFAULT_FRAME_DAMP = 1

    def __init__(self, pixels: float, fov: float) -> None:
        """class to be used for storing limits of an optical observation system

        :param pixels: 1-D full width pixel count assuming a square sensor
        :type pixels: float
        :param fov: half-angle field-of-view in radians
        :type fov: float
        """
        #: minimum sun angle from sensor bore to prevent damage (radians)
        self.sun_hard: float = OpticalConstraints.DEFAULT_SUN_HARD

        #: minimum sun angle from bore to enable detection (radians)
        self.sun_soft: float = OpticalConstraints.DEFAULT_SUN_SOFT

        #: minimum moon angle from bore to enable detection (radians)
        self.moon: float = OpticalConstraints.DEFAULT_MOON_LIMIT

        #: minimum earth angle from bore to enable detection (radians)
        self.earth: float = OpticalConstraints.DEFAULT_EARTH_LIMIT

        #: limiting visual magnitude of the sensor (higher means the sensor will detect dimmer objects)
        self.vismag: float = OpticalConstraints.DEFAULT_LIMITING_MAG

        #: maximum angle an object can be from the center of the sensor (radians)
        self.bore: float = OpticalConstraints.DEFAULT_FRAME_DAMP * fov

        clos: float = OpticalConstraints.DEFAULT_RESOLUTION_LIMIT * 2 * pixels

        #: maximum range an object can be away for successful characterization (km)
        self.characterization: float = clos / tan(fov)
