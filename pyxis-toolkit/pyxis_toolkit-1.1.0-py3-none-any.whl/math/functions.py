from math import cos, radians, sin
from typing import List

from pyxis.math.constants import HOURS_IN_DAY, MINUTES_IN_DAY, MINUTES_IN_HOUR, SECONDS_IN_DAY, SECONDS_IN_HOUR


class Conversions:
    """class used to perform various unit conversions

    :return: defined by each static method
    :rtype: defined by each static method
    """

    @staticmethod
    def hms_to_decimal_day(hr: float, m: float, s: float) -> float:
        """calculate the float value of the day given an hour, minute, second representation

        :param hr: hour of day
        :type hr: float
        :param m: minute of day
        :type m: float
        :param s: second of day
        :type s: float
        :return: the time in days
        :rtype: float
        """
        return hr / HOURS_IN_DAY + m / MINUTES_IN_DAY + s / SECONDS_IN_DAY

    @staticmethod
    def dms_to_radians(d: float, m: float, s: float) -> float:
        """calculate an angle in radians that has been defined in degrees, minutes, and seconds

        :param d: degrees in angle
        :type d: float
        :param m: minute of angle
        :type m: float
        :param s: second of angle
        :type s: float
        :return: angle in radians
        :rtype: float
        """
        return radians(d + m / MINUTES_IN_HOUR + s / SECONDS_IN_HOUR)


def sign(num: float) -> float:
    """function to determine if a value is positive or negative

    :param num: expression to be signed
    :type num: float
    :return: 1 if positive -1 if negative 0 if neither
    :rtype: float
    """
    val = 0
    if num > 0:
        val = 1
    elif num < 0:
        val = -1
    return val


class LegendrePolynomial:
    def __init__(self, phi: float) -> None:
        """stores the explicit solution to normalized legendre polynomials used in the geopotential calculations

        :param phi: geodetic latitude in radians
        :type phi: float
        """
        cos_phi: float = cos(phi)
        sin_phi: float = sin(phi)
        cos_phi_squared: float = cos_phi * cos_phi
        sin_phi_squared: float = sin_phi * sin_phi

        #: the polynomial list of lists with indices n, m
        self.p: List[List[float]] = [
            [1, 0],
            [sin_phi, cos_phi, 0],
            [
                (3 * sin_phi_squared - 1) * 0.5,
                3 * sin_phi * cos_phi,
                3 * cos_phi_squared,
                0,
            ],
            [
                sin_phi * (5 * sin_phi_squared - 3) * 0.5,
                (15 * sin_phi_squared - 3) * cos_phi * 0.5,
                15 * sin_phi * cos_phi_squared,
                15 * cos_phi_squared * cos_phi,
                0,
            ],
            [
                0.125 * (35 * sin_phi_squared * sin_phi_squared - 30 * sin_phi_squared + 3),
                2.5 * (7 * sin_phi_squared * sin_phi - 3 * sin_phi) * cos_phi,
                (7 * sin_phi_squared - 1) * cos_phi_squared * 7.5,
                105 * cos_phi * cos_phi_squared * sin_phi,
                105 * cos_phi_squared * cos_phi_squared,
                0,
            ],
        ]
