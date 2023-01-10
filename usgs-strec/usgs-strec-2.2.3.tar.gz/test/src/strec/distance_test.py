#!/usr/bin/env python

# stdlib imports
import json
import pathlib
import sys

# third party imports
from shapely.geometry import Point, shape

# local imports
from strec.distance import calc_distances, get_distance_to_regime


def print_dict(dict):
    for key, value in dict.items():
        print(f"{key} = {value:.1f} km")


def test_calc_tectonic_distances():

    points = [
        {
            "name": "Big Island",
            "region": "HotSpot",
            "lat": 19.630525,
            "lon": -155.435738,
            "order": [
                "DistanceToHotSpot",
                "DistanceToStable",
                "DistanceToActive",
                "DistanceToSubduction",
            ],
        },
        {
            "name": "Valparaiso, Chile",
            "region": "Subduction",
            "lat": -33.045879,
            "lon": -71.624954,
            "order": [
                "DistanceToSubduction",
                "DistanceToActive",
                "DistanceToHotSpot",
                "DistanceToStable",
            ],
        },
        {
            "name": "Coast of Greenland",
            "region": "Stable",
            "lat": 68.626508,
            "lon": -29.261091,
            "order": [
                "DistanceToStable",
                "DistanceToActive",
                "DistanceToHotSpot",
                "DistanceToSubduction",
            ],
        },
        {
            "name": "Tierra del Fuego",
            "region": "Active",
            "lat": -54.816815,
            "lon": -65.554447,
            "order": [
                "DistanceToActive",
                "DistanceToStable",
                "DistanceToHotSpot",
                "DistanceToSubduction",
            ],
        },
    ]

    for pdict in points:
        print(
            (
                f"Checking point ({pdict['lat']}, {pdict['lon']}) "
                f"{pdict['name']}, should be {pdict['region']}"
            )
        )
        distances = calc_distances(pdict["lat"], pdict["lon"])
        distances.pop("DistanceToOceanic", None)
        distances.pop("DistanceToContinental", None)
        sorted_distances = {
            k: v for k, v in sorted(distances.items(), key=lambda item: item[1])
        }
        cmp_order = list(sorted_distances.keys())
        print_dict(sorted_distances)
        print()
        assert pdict["order"] == cmp_order

    stable_points = [
        (40.964218, -95.890236),
        (35.958876, -83.608163),
        (52.633529, -105.613543),
        (51.771052, 18.998324),
        (8.105838, -6.461390),
        (-27.008106, 133.031058),
        (15.494769, 76.482348),
        (22.387245, 46.416856),
    ]
    for lat, lon in stable_points:
        distances = calc_distances(lat, lon)
        print(f"Checking stable point {lat},{lon}...")
        assert distances["DistanceToStable"] == 0

    active_points = [
        (35.701466, -120.115478),
        (21.300028, -77.624746),
        (29.077189, 26.729212),
        (36.175032, 55.557337),
        (-58.0, 149.7),
    ]
    for lat, lon in active_points:
        distances = calc_distances(lat, lon)
        assert distances["DistanceToActive"] == 0

    subduction_points = [
        (17.44, -98.49),
        (-15.52, -70.49),
        (34.39, -5.68),
        (35.70, 23.82),
        (-6.07, 126.74),
        (-39.50, 176.18),
        (45.93, 146.59),
        (51.81, 175.36),
    ]
    for lat, lon in subduction_points:
        distances = calc_distances(lat, lon)
        print(f"Checking subduction point {lat},{lon}...")
        assert distances["DistanceToSubduction"] == 0

    volcanic_points = [
        (19.723, -155.681),
        (45.73, -129.93),
        (-0.54, -90.03),
        (64.714, -18.394),
        (7.23, 38.37),
        (-63.76, -57.37),
        (-49.58, 69.12),
        (-37.64, 142.46),
    ]
    for lat, lon in volcanic_points:
        distances = calc_distances(lat, lon)
        assert distances["DistanceToHotSpot"] == 0


def test_calc_oceanic_distances():
    points = [
        {
            "name": "Madagascar",
            "region": "Continental",
            "lat": -13.356,
            "lon": 48.272,
            "order": [
                "DistanceToContinental",
                "DistanceToOceanic",
            ],
        },
        {
            "name": "United States",
            "region": "Continental",
            "lat": 43.41,
            "lon": -102.19,
            "order": [
                "DistanceToContinental",
                "DistanceToOceanic",
            ],
        },
        {
            "name": "Iceland",
            "region": "Oceanic",
            "lat": 64.878,
            "lon": -24.051,
            "order": [
                "DistanceToOceanic",
                "DistanceToContinental",
            ],
        },
        {
            "name": "South Pacific",
            "region": "Oceanic",
            "lat": -19.98,
            "lon": -105.38,
            "order": [
                "DistanceToOceanic",
                "DistanceToContinental",
            ],
        },
    ]
    for pdict in points:
        print(
            (
                f"Checking point ({pdict['lat']}, {pdict['lon']}) "
                f"{pdict['name']}, should be {pdict['region']}"
            )
        )
        distances = calc_distances(pdict["lat"], pdict["lon"])
        distances.pop("DistanceToActive", None)
        distances.pop("DistanceToStable", None)
        distances.pop("DistanceToSubduction", None)
        distances.pop("DistanceToHotSpot", None)
        sorted_distances = {
            k: v for k, v in sorted(distances.items(), key=lambda item: item[1])
        }
        cmp_order = list(sorted_distances.keys())
        print_dict(sorted_distances)
        print()
        assert pdict["order"] == cmp_order

    land_points = [
        (38.397633, -103.922577),
        (19.627053, -100.231171),
        (-5.457441, -61.559299),
        (21.110111, 12.444609),
        (-74.216469, 22.464139),
        (-22.608953, 124.944608),
        (-12.010521, 124.976613),
        (36.212620, 97.557150),
        (80.653060, 95.339942),
        (51.147136, 19.052844),
    ]
    for lat, lon in land_points:
        distances = calc_distances(lat, lon)
        assert distances["DistanceToContinental"] == 0.0

    ocean_points = [
        (46.393396, -138.365785),
        (44.107786, -125.987451),
        (-45.895658, -114.550334),
        (-20.972943, -74.749524),
        (-53.472616, 3.515289),
        (0, 0),
        (44.068439, -36.067652),
        (81.286241, -0.643259),
        (81.612268, 127.956193),
        (-43.702279, 155.658387),
    ]
    for lat, lon in ocean_points:
        distances = calc_distances(lat, lon)
        assert distances["DistanceToOceanic"] == 0.0


def test_get_regime_distance():
    # these are in lon,lat order
    hotspots = [
        (-30, 38.6),
        (-16.71, 32.83),
        (-16.71, 28.99),
        (-24.42, 15.78),
        (-29.08, -20.04),
        (-80.49, -26.01),
        (-89.46, -0.05),
        (-170.22, -14.30),
        (-111.05, 44.45),
    ]

    stables = [
        (-32.0, -63.298),
        (-62.13, -23.50),
        (-109.70, 43.80),
        (-118.57, 89.14),
        (-55.92, -89.75),
        (-60.0, -15.0),
    ]

    actives = [
        (-14.55, -8.80),
        (-17.648, -11.407),
        (-62.870, -23.630),
        (-110.91, 42.91),
    ]

    subductions = [
        (-74.316, -36.624),
        (-30.006, -56.368),
        (121.053, -11.288),
        (120.351, 20.814),
        (-179.960, 51.273),
        (179.955, 51.150),
    ]

    for lon, lat in hotspots:
        print(f"Checking ({lat},{lon}) is hotspot...")
        distance = get_distance_to_regime(lat, lon, "volcanic")
        assert distance == 0.0
    for lon, lat in stables:
        print(f"Checking ({lat},{lon}) is stable...")
        distance = get_distance_to_regime(lat, lon, "stable")
        assert distance == 0.0
    for lon, lat in actives:
        print(f"Checking ({lat},{lon}) is active...")
        distance = get_distance_to_regime(lat, lon, "active")
        assert distance == 0.0
    for lon, lat in subductions:
        print(f"Checking ({lat},{lon}) is subduction...")
        distance = get_distance_to_regime(lat, lon, "subduction")
        assert distance == 0.0


def test_distances_along_lat():
    tlat = -21.326
    points = [
        (-65.531, tlat, "DistanceToSubduction"),
        (-63.173, tlat, "DistanceToSubduction"),
        (-62.904, tlat, "DistanceToSubduction"),
        (-62.652, tlat, "DistanceToActive"),
        (-62.242, tlat, "DistanceToActive"),
        (-61.960, tlat, "DistanceToActive"),
        (-61.837, tlat, "DistanceToStable"),
        (-61.656, tlat, "DistanceToStable"),
        (-61.445, tlat, "DistanceToStable"),
        (-61.122, tlat, "DistanceToStable"),
        (-60.378, tlat, "DistanceToStable"),
        (-59.822, tlat, "DistanceToStable"),
        (-56.070, tlat, "DistanceToStable"),
        (-58.57, 13.66, "DistanceToSubduction"),
        (-57.16, 13.66, "DistanceToActive"),
        (-55.93, 13.66, "DistanceToStable"),
    ]
    for lon, lat, rtype in points:
        distances = calc_distances(lat, lon)
        distances.pop("DistanceToContinental")
        distances.pop("DistanceToOceanic")
        ctype = min(distances, key=distances.get)
        print(min(distances.values()))
        if rtype != ctype:
            rdist = distances[rtype]
            cdist = distances[ctype]
            print(
                f"Point ({lat},{lon}) should be {rtype} ({rdist:.2f}), came back as {ctype} ({cdist:.2f})."
            )


if __name__ == "__main__":
    test_calc_tectonic_distances()
    test_distances_along_lat()
    test_get_regime_distance()
    test_calc_tectonic_distances()
    test_calc_oceanic_distances()
