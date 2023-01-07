#!/usr/bin/env python

# stdlib imports
import pathlib

# third party imports
import numpy as np

# local imports
from esi_utils_pager.exposure import Exposure, calc_exposure
from esi_utils_pager.growth import PopulationGrowth


def basic_test():
    print("Testing very basic exposure calculation...")
    mmidata = np.array(
        [
            [7, 8, 8, 8, 7],
            [8, 9, 9, 9, 8],
            [8, 9, 10, 9, 8],
            [8, 9, 9, 8, 8],
            [7, 8, 8, 6, 5],
        ],
        dtype=np.float32,
    )
    popdata = np.ones_like(mmidata) * 1e7
    isodata = np.array(
        [
            [4, 4, 4, 4, 4],
            [4, 4, 4, 4, 4],
            [4, 4, 156, 156, 156],
            [156, 156, 156, 156, 156],
            [156, 156, 156, 156, 156],
        ],
        dtype=np.int32,
    )
    expdict = calc_exposure(mmidata, popdata, isodata)
    testdict = {
        4: np.array([0, 0, 0, 0, 0, 0, 2e7, 6e7, 4e7, 0]),
        156: np.array([0, 0, 0, 0, 1e7, 1e7, 1e7, 6e7, 3e7, 1e7]),
    }

    for ccode, value in expdict.items():
        testvalue = testdict[ccode]
        np.testing.assert_almost_equal(value, testvalue)

    print("Passed very basic exposure calculation...")


def test():
    print("Testing Northridge exposure check (with GPW data).")
    events = ["northridge"]
    homedir = pathlib.Path(__file__).parent  # where is this script?
    for event in events:
        shakefile = homedir / "data" / f"{event}_grid.xml"
        popfile = homedir / "data" / f"{event}_gpw.flt"
        isofile = homedir / "data" / f"{event}_isogrid.bil"
        exp = Exposure(popfile, 2012, isofile)
        results = exp.calcExposure(shakefile)
        cmpexposure = [0, 0, 1817, 1767260, 5840985, 5780298, 2738374, 1559657, 4094, 0]
        np.testing.assert_almost_equal(cmpexposure, results["TotalExposure"])
    print("Passed Northridge exposure check (with GPW data).")


if __name__ == "__main__":
    basic_test()
    test()
