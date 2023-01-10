#!/usr/bin/env python
# stdlib imports
import pathlib

# third party imports
import numpy as np

# local imports
from strec.slab import GridSlab, SlabCollection


def test_grid_slab():
    homedir = pathlib.Path(__file__).parent  # where is this script?
    datadir = (
        homedir / ".." / ".." / ".." / "src" / "strec" / "data" / "slabs"
    ).resolve()  # all slabs should be here
    depthgrid = datadir / "kur_slab2_dep_02.24.18.grd"
    dipgrid = datadir / "kur_slab2_dip_02.24.18.grd"
    strgrid = datadir / "kur_slab2_str_02.24.18.grd"
    uncgrid = datadir / "kur_slab2_unc_02.24.18.grd"
    grid = GridSlab(depthgrid, dipgrid, strgrid, uncgrid)
    is_inside = grid.contains(40.0, 140.0)
    assert is_inside

    slabinfo = grid.getSlabInfo(40.0, 140.0)
    if not len(slabinfo):
        raise AssertionError("Slab results are empty!")
    cmp_dict = {
        "dip": 28.817652,
        "depth": 127.33068084716797,
        "depth_uncertainty": 16.426598,
        "strike": 186.17316,
        "region": "kur",
        "maximum_interface_depth": 54,
    }
    for key, value in cmp_dict.items():
        value2 = slabinfo[key]
        print(f"Comparing {key} cmp {value} and actual {value2}")
        if isinstance(value, float):
            np.testing.assert_almost_equal(value, value2, decimal=4)
        else:
            assert value == value2


def test_inside_grid():
    homedir = pathlib.Path(__file__).parent  # where is this script?
    datadir = (
        homedir / ".." / ".." / ".." / "src" / "strec" / "data" / "slabs"
    ).resolve()  # all slabs should be here
    collection = SlabCollection(datadir)
    lat = 10.0
    lon = 126.0
    depth = 0.0
    slabinfo = collection.getSlabInfo(lat, lon, depth)
    if not len(slabinfo):
        raise AssertionError("Slab results are empty!")
    test_slabinfo = {
        "maximum_interface_depth": 49,
        "depth": 67.86959075927734,
        "strike": 159.2344,
        "dip": 45.410145,
        "depth_uncertainty": 14.463925,
        "region": "phi",
    }
    print("Testing against slab grid...")
    for key, value in slabinfo.items():
        assert key in test_slabinfo
        if isinstance(value, str):
            assert value == test_slabinfo[key]
        else:
            np.testing.assert_almost_equal(value, test_slabinfo[key], decimal=1)
    print("Passed.")


if __name__ == "__main__":
    test_grid_slab()
    test_inside_grid()
