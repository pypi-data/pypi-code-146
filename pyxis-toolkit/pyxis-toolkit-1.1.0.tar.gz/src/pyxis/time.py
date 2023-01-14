from math import floor, radians

from pyxis.math.constants import SECONDS_IN_DAY
from pyxis.math.functions import Conversions


class Epoch:

    #: julian value to act as the MJD start
    MJD_ZERO = 2400000.5

    #: number of days in a julian century
    JULIAN_CENTURY = 36525

    #: julian value for the j2000 epoch
    J2000_JULIAN_DATE = 2451545

    #: offset in days of the universal coordinated time system and the terrestrial dynamic time system
    UTC_TDT_OFFSET = 69.184 / SECONDS_IN_DAY

    def __init__(self, value: float) -> None:
        """class used to represent time

        :param value: time in modified julian days
        :type value: float
        """
        self.value = value

    def copy(self) -> "Epoch":
        """used to create a copy of the current epoch

        :return: a replica of the calling epoch
        :rtype: Epoch
        """
        return Epoch(self.value)

    @classmethod
    def from_gregorian(cls, year: int, month: int, day: int, hour: int, minute: int, sec: float) -> "Epoch":
        """instantiate an epoch from the standard calendar format

        :param year: 4-digit year
        :type year: int
        :param month: 2-digit month
        :type month: int
        :param day: 2-digit day
        :type day: int
        :param hour: 2-digit hour
        :type hour: int
        :param minute: 2-digit minute
        :type minute: int
        :param sec: 2-digit and trailing decimal second
        :type sec: float
        :return: epoch with an mjd value equivalent to the corresponding calendar date
        :rtype: Epoch
        """
        y = year
        m = month
        d = day

        if m <= 2:
            y -= 1
            m += 12

        b = floor(y / 400) - floor(y / 100) + floor(y / 4)
        mjd = 365 * y - 679004 + b + floor(30.6001 * (m + 1)) + d

        return cls(mjd + Conversions.hms_to_decimal_day(hour, minute, sec))

    def julian_value(self) -> float:
        """calculate the julian value of the calling epoch

        :return: full julian date
        :rtype: float
        """
        return self.value + self.MJD_ZERO

    def julian_centuries_past_j2000(self) -> float:
        """calculate the number of julian centuries that have elapsed since the j2000 epoch

        :return: number of julian centuries past the j2000 epoch
        :rtype: float
        """
        return (self.julian_value() - self.J2000_JULIAN_DATE) / self.JULIAN_CENTURY

    def plus_days(self, t: float) -> "Epoch":
        """calculate an epoch that is separated from the calling epoch by t days

        :param t: time delta of the two epochs in days
        :type t: float
        :return: an epoch that is t days away from the calling epoch
        :rtype: Epoch
        """
        return Epoch(self.value + t)

    def greenwich_hour_angle(self) -> float:
        """calculate the greenwich hour angle used to determine sidereal time

        :return: greenwich mean sidereal time in radians
        :rtype: float
        """
        # solve for julian centuries since j2000 using equation 2.7
        utc = Epoch(self.value - Epoch.UTC_TDT_OFFSET)
        dec_day = utc.value % 1
        j0 = utc.julian_value() - dec_day
        j = (j0 - Epoch.J2000_JULIAN_DATE) / Epoch.JULIAN_CENTURY

        # solve for theta0 using equation 2.6
        theta0 = 100.4606184 + 36000.77004 * j + 0.000387933 * j * j

        # solve for gmst using equation 2.8
        total_deg = theta0 + 360.98564724 * dec_day
        return radians(total_deg % 360)
