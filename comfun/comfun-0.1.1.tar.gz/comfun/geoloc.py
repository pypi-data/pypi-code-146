#!/usr/bin/env python3

import math
from typing import Tuple

def DD_to_DMS(latlon_DD: Tuple[float], return_as_str=False):
    """
    Assumes positive N/S values for northern hemisphere and negative values for southern hemisphere.
    Similarly, positive values for eastern hemisphere, negative values for western hemisphere.
    :param dd_NS_EW: tuple (north/south, east/west)
    :return:
    """

    DMS = []
    for dimension, value in zip(("lat", "lon"), latlon_DD):

        if  dimension == "lat" and value >= 0:
            hemisphere = "N"
        elif dimension == "lat" and value < 0:
            hemisphere = "S"
        elif dimension == "lon" and value >= 0:
            hemisphere = "E"
        else:
            hemisphere = "W"

        degrees = math.floor(abs(value))
        dec_min = (abs(value) % degrees) * 60
        minutes = math.floor(dec_min)
        seconds = (dec_min % minutes) * 60

        if return_as_str:
            DMS.append(f"""{degrees}°{minutes}'{seconds}"{hemisphere}""")
        else:
            DMS.append((degrees, minutes, seconds, hemisphere))

    return DMS


def DMS_to_DD(degminsec):
    # ToDo: take either tuples (deg, min, sec) or str ("deg°min'sec"")
    pass


if __name__ == "__main__":
    DD = (-35.902596320663314, 14.52547744715463)
    DMS = DD_to_DMS(DD, return_as_str=True)
    with open("/home/findux/Desktop/coords.csv", "a") as f:
        f.writelines([e + "\n" for e in DMS])

