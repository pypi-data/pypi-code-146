from collections import namedtuple
from enum import Enum


Geocode = namedtuple("Geocode", ["location", "location_type", "viewport"])
Location = namedtuple(
    "Location",
    ["city", "country", "formatted_address", "place_id", "postcode", "region"],
)
Point = namedtuple("Point", ["latitude", "longitude"])


class Viewport(namedtuple("Viewport", ["southwest", "northeast"])):
    def __contains__(self, point):
        """A Point is in the Viewport when its lat/long coordinates are within the SW/NE bounding
        box.

        Latitude
               ^
               |              NE
               +-----+-------+
               |     |       |
               x--------P    |
               |     |  |    |
               +-----+--|----+
               |   SW|  |    |
               o-----+--x----+----------> Longitude

        """
        if type(point) is Point:
            return all(
                [
                    point.latitude >= self.southwest.latitude,
                    point.latitude <= self.northeast.latitude,
                    point.longitude >= self.southwest.longitude,
                    point.longitude <= self.northeast.longitude,
                ]
            )

        return False


class Geotype(Enum):
    ROOFTOP = (
        "Indicates that the returned result is a precise geocode for which we have location "
        "information accurate down to street address precision."
    )
    RANGE_INTERPOLATED = (
        "Indicates that the returned result reflects an approximation (usually on a road) "
        "interpolated between two precise points (such as intersections). Interpolated results "
        "are generally returned when rooftop geocodes are unavailable for a street address."
    )
    GEOMETRIC_CENTER = (
        "Indicates that the returned result is the geometric center of a result such as a "
        "polyline (for example, a street) or polygon (region)."
    )
    APPROXIMATE = "Indicates that the returned result is approximate."
    MANUAL = "Indicates that the Coordinates were added manually."
    MISSING = "Indicates that a result would not be found."
    MULTIPLE = "Indicates that the Coordinates are an alternative location for an existing location."
