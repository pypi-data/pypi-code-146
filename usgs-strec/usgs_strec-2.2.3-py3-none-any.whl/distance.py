# stdlib imports
import json
import pathlib
import warnings
from datetime import datetime

# third party imports
import pyproj
from geopy.distance import distance as geodetic
from shapely.geometry import Point, shape
from shapely.ops import transform

# local imports
from strec.utils import get_config

CENTROID_MAX_DISTANCE = 6200  # approx length of largest subduction zone (SAM)
TECTONIC_REGIONS = {
    "stable": "DistanceToStable",
    "active": "DistanceToActive",
    "volcanic": "DistanceToHotSpot",
    "subduction": "DistanceToSubduction",
    "ocean": "DistanceToOceanic",
    "land": "DistanceToContinental",
}


def get_distance_to_shape(polygon_shape, clat, clon, dest_crs, regime):
    """Calculate distance to input geometry from lat/lon in given projection.

    Args:
        cutshape (shapely Geometry): Shape (usually Polygon) to calculate distance to.
        clat (float): Earthquake latitude.
        clon (float): Earthquake longitude.
        projection (Proj): Proj4 class defining an input projection.
    Returns:
        float: Distance in km from shape to lat/lon.
    """
    geo_crs = pyproj.CRS("EPSG:4326")
    pfunction = pyproj.Transformer.from_crs(geo_crs, dest_crs, always_xy=True).transform
    point = Point(clon, clat)
    proj_point = transform(pfunction, point)
    proj_shape = transform(pfunction, polygon_shape)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        distance = proj_shape.distance(proj_point) / 1000

    return distance


def get_distance_to_regime(lat, lon, regime):
    """Calculate distance from point to nearest polygon in a given regime.

    Args:
        lat (float): Earthquake latitude.
        lon (float): Earthquake longitude.
        regime (str): One of ["land", "ocean", "active", "stable", "hotspot", "subduction"]
    Returns:
        float: Distance (km) to nearest regime polygon.
    """
    config = get_config()
    longest_axis = float(config["DATA"]["longest_axis"])
    ortho_crs = pyproj.CRS(f"+proj=aeqd +lon_0={lon:.6f} +lat_0={lat:.6f} +ellps=WGS84")
    root = pathlib.Path(__file__).parent / "data"
    mindist = 1e9
    datafile = root / f"{regime}.geojson"
    with open(datafile, "rt") as f:
        jdict = json.load(f)
    for feature in jdict["features"]:
        geometry = shape(feature["geometry"])
        cx, cy = geometry.centroid.xy
        cdist = geodetic((lat, lon), (cy[0], cx[0])).km
        if cdist > longest_axis:
            continue
        dist = get_distance_to_shape(geometry, lat, lon, ortho_crs, regime)
        if dist < mindist:
            mindist = dist

    return mindist


def calc_distances(lat, lon):
    """Calculate distances from input lat/lon to nearest tectonic regime polygons.

    Args:
        lat (float): Earthquake latitude.
        lon (float): Earthquake longitude.
    Returns:
        dict: Dictionary of distances in km:
              - DistanceToActive
              - DistanceToStable
              - DistanceToSubduction
              - DistanceToHotSpot
              - DistanceToOceanic
              - DistanceToContinental
    """
    distances = {}
    regimes = ["active", "stable", "subduction", "volcanic", "ocean", "land"]
    for regime in regimes:
        mindist = get_distance_to_regime(lat, lon, regime)
        distances[regime] = mindist

    for oldkey, newkey in TECTONIC_REGIONS.items():
        if oldkey not in distances:
            continue
        distances[newkey] = distances[oldkey]
        del distances[oldkey]

    return distances
