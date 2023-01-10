#!/usr/bin/env python

from strec.gmreg import Regionalizer


def test_regionalizer():
    regionalizer = Regionalizer.load()

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
        results = regionalizer.getRegions(lat, lon)
        assert results["TectonicRegion"] == "HotSpot"
    for lon, lat in stables:
        print(f"Checking ({lat},{lon}) is stable...")
        results = regionalizer.getRegions(lat, lon)
        assert results["TectonicRegion"] == "Stable"
    for lon, lat in actives:
        print(f"Checking ({lat},{lon}) is active...")
        results = regionalizer.getRegions(lat, lon)
        assert results["TectonicRegion"] == "Active"
    for lon, lat in subductions:
        print(f"Checking ({lat},{lon}) is subduction...")
        results = regionalizer.getRegions(lat, lon)
        assert results["TectonicRegion"] == "Subduction"


if __name__ == "__main__":
    test_regionalizer()
