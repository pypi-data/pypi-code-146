#!/usr/bin/python

# third party imports
import numpy as np

RESOLUTIONS = ["cardinal", "intercardinal", "meteorological"]

LONG_CARDINAL_POINTS = ["North", "East", "South", "West", "North"]
SHORT_CARDINAL_POINTS = ["N", "E", "S", "W", "N"]

LONG_INTERCARDINAL_POINTS = [
    "North",
    "Northeast",
    "East",
    "Southeast",
    "South",
    "Southwest",
    "West",
    "Northwest",
    "North",
]
SHORT_INTERCARDINAL_POINTS = ["N", "NE", "E", "SE", "S", "SW", "W", "NW", "N"]

LONG_METEOROLOGICAL_POINTS = [
    "North",
    "North-northeast",
    "Northeast",
    "East-northeast",
    "East",
    "East-southeast",
    "Southeast",
    "South-southeast",
    "South",
    "South-southwest",
    "Southwest",
    "West-southwest",
    "West",
    "West-northwest",
    "Northwest",
    "North-northwest",
    "North",
]
SHORT_METEOROLOGICAL_POINTS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
    "N",
]


def azimuth(lat1, lon1, lat2, lon2):
    # adapted from https://www.movable-type.co.uk/scripts/latlong.html
    lat1r = np.radians(lat1)
    lon1r = np.radians(lon1)
    lat2r = np.radians(lat2)
    lon2r = np.radians(lon2)
    y = np.sin(lon2r - lon1r) * np.cos(lat2r)
    x = np.cos(lat1r) * np.sin(lat2r) - np.sin(lat1r) * np.cos(lat2r) * np.cos(
        lon2r - lon1r
    )
    theta = np.arctan2(y, x)
    # bearing in degrees
    bearing = (np.degrees(theta) + 360) % 360
    return bearing


def get_compass_dir(lat1, lon1, lat2, lon2, resolution="intercardinal", format="short"):
    """Get the nearest string compass direction between two points.

    Args:
        lat1 (float): Latitude of first point.
        lon1 (float): Longitude of first point.
        lat2 (float): Latitude of second point.
        lon2 (float): Longitude of second point.
        resolution (str): One of ['cardinal', 'intercardinal', 'meteorological'].
        format (str): String used to determine the type of output. ('short','long').

    Returns:
        str: String compass direction, in the form of 'North','Northeast',... if format is 'long',
             or 'N','NE',... if format is 'short'.
    """
    az = azimuth(lon1, lat1, lon2, lat2)
    if az < 0:
        az += 360
    return get_compass_dir_azimuth(az, resolution=resolution)


def get_compass_dir_azimuth(azimuth, resolution="intercardinal", format="short"):
    """Get the nearest string compass direction between two points.
    Args:
        azimuth (float): Numerical compass direction between two points.
        resolution (str): One of ['cardinal', 'intercardinal', 'meteorological'].
        format (str): String used to determine the type of output. ('short','long').

    Returns:
        str: String compass direction, in the form of 'North','Northeast',... if format is 'long',
             or 'N','NE',... if format is 'short'.
    """
    if azimuth < 0:
        azimuth += 360
    if format not in ["short", "long"]:
        raise KeyError(f"Direction format {format} is not supported")
    if resolution not in ["cardinal", "intercardinal", "meteorological"]:
        raise KeyError(f"Direction resolution {resolution} is not supported")
    if resolution == "cardinal":
        angles = np.arange(0, 360 + 90, 90)
        if format == "long":
            points = LONG_CARDINAL_POINTS
        else:
            points = SHORT_CARDINAL_POINTS
    elif resolution == "intercardinal":
        angles = np.arange(0, 360 + 45, 45)
        if format == "long":
            points = LONG_INTERCARDINAL_POINTS
        else:
            points = SHORT_INTERCARDINAL_POINTS
    elif resolution == "meteorological":
        angles = np.arange(0, 360 + 22.5, 22.5)
        if format == "long":
            points = LONG_METEOROLOGICAL_POINTS
        else:
            points = SHORT_METEOROLOGICAL_POINTS

    adiff = abs(azimuth - angles)
    i = adiff.argmin()
    return points[i]
