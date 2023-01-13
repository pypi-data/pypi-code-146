from __future__ import annotations
from enum import Enum
from typing import Tuple

import numpy as np
from sklearn.metrics.pairwise import haversine_distances

from mfire.settings import Settings, TEMPLATES_FILENAMES
from mfire.settings.constants import EARTH_RADIUS_KM
from mfire.utils import JsonFile

Point = Tuple[float, float]
Angle = float

DIR_DICT = JsonFile(TEMPLATES_FILENAMES[Settings().language]["compass"]).load()


class _CompassRoseMixin(Angle):
    """Mixin class for implementing basic compass rose handling.
    This mixin extends the float class must be coupled with an Enum class
    to properly work.

    Inheritance:
        - Angle (aka float)
    """

    def __eq__(self, __x: object) -> bool:
        return super().__eq__(__x % 360)

    @classmethod
    def from_azimut(cls, azimut: Angle) -> _CompassRoseMixin:
        """Class method for returning the compass direction associated to
        the given azimut.

        Args:
            azimut (Angle): Azimut angle in degrees.

        Returns:
            _CompassRoseMixin: Direction associated to the given azimut.
        """
        return min(
            (min(abs(d + 360 - azimut % 360), abs(d - azimut % 360)), d) for d in cls
        )[1]

    @property
    def opposite(self) -> _CompassRoseMixin:
        """Returns the opposite direction of self.

        Returns:
            _CompassRoseMixin: Opposite direction.
        """
        return self.from_azimut(self + 180)

    @property
    def _text_elements(self) -> list:
        """Retrieves the textual description settings of compass.
        We use the constant dictionnary DIR_DICT, loaded from the config file
        in TEMPLATES_FILENAMES[language]["compass"].

        Returns:
            list: List of textual descriptions elements
        """
        return DIR_DICT[self.name]

    @property
    def description(self) -> str:
        """Textual description of the compass direction. E.g. "Nord" for the direction
        corresponding to the class "N" in french.
        """
        return self._text_elements[0]

    @property
    def short_description(self) -> str:
        """Short description of the compass direction. E.g. "N" for the direction
        corresponding to the class "N" in french.
        """
        return self._text_elements[1]

    @property
    def text(self) -> str:
        """Nominal group describing a specific compass direction. E.g. "le Nord" for the
        direction corresponding to the class "N" in french.
        """
        return f"{self._text_elements[-1]}{self.description}"

    @classmethod
    def azimut(cls, p1: Point, p2: Point) -> Angle:
        """
        Un azimut entre 2 points est l'angle formé par la droite passant par
        les 2 points et la ligne passant par les 2 pôles.
        Retourne l'angle en degré.
        Permet de déterminer le sens de déplacement des objets.

        Args:
            p1 (Point): (lon, lat) coordinates of the first point.
            p2 (Point): (lon, lat) coordinates of the second point.

        Returns:
            Angle: Azimut angle of the segment going from p1 to p2.
        """
        lon1, lat1, lon2, lat2 = np.radians((p1, p2)).reshape(-1)
        x = np.cos(lat1) * np.sin(lat2) - np.sin(lat1) * np.cos(lat2) * np.cos(
            lon2 - lon1
        )
        y = np.sin(lon2 - lon1) * np.cos(lat2)
        return np.degrees(np.arctan2(y, x))

    @classmethod
    def from_points(cls, p1: Point, p2: Point) -> _CompassRoseMixin:
        """Class method returning a compass direction out of 2 points. The result
        corresponds to the direction of the segment going from p1 to p2.

        Args:
            p1 (Point): (lon, lat) coordinates of the first point.
            p2 (Point): (lon, lat) coordinates of the second point.

        Returns:
            _CompassRoseMixin: Direction class of the segment going from p1 to p2.
        """
        return cls.from_azimut(cls.azimut(p1, p2))


class CompassRose8(_CompassRoseMixin, Enum):
    """Enum class representing an 8-point compass rose.

    Inheritance:
        _CompassRoseMixin
        Enum
    """

    N = 0
    NE = 45
    E = 90
    SE = 135
    S = 180
    SW = 225
    W = 270
    NW = 315


class CompassRose16(_CompassRoseMixin, Enum):
    """Enum class representing an 16-point compass rose.

    Inheritance:
        _CompassRoseMixin
        Enum
    """

    N = 0
    NNE = 22.5
    NE = 45
    ENE = 67.5
    E = 90
    ESE = 112.5
    SE = 135
    SSE = 157.5
    S = 180
    SSW = 202.5
    SW = 225
    WSW = 247.5
    W = 270
    WNW = 292.5
    NW = 315
    NNW = 337.5


def distance_on_earth(p1: Point, p2: Point) -> float:
    """Distance between two (lon, lat) points on earth in km

    Args:
        p1 (Tuple[float, float]): (lon, lat) coordinates of point 1
        p2 (Tuple[float, float]): (lon, lat) coordinates of point 2

    Returns:
        float: Distance in km between the two given points
    """
    return (haversine_distances(np.radians((p1, p2))[:, ::-1]) * EARTH_RADIUS_KM)[0, 1]
