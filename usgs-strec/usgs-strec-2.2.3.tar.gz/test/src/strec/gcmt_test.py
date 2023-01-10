#!/usr/bin/env python

# stdlib imports
import os.path
import pathlib
from datetime import datetime

# third party imports
from esi_utils_rupture.tensor import fill_tensor_from_components

# remove later
from strec.gcmt import fetch_gcmt, ndk_to_dataframe
from strec.subtype import get_focal_mechanism


def throw_away():
    dataframe = fetch_gcmt()
    mechs = []
    for idx, row in dataframe.iterrows():
        tensor = fill_tensor_from_components(
            row["mrr"], row["mtt"], row["mpp"], row["mrt"], row["mrp"], row["mtp"]
        )
        mech = get_focal_mechanism(tensor)
        mechs.append(mech)
    dataframe["focal_mechanism"] = mechs
    try:
        dataframe.to_excel("gcmt_mechanisms.xlsx")
    except Exception as e:
        raise e
    finally:
        os.remove("gcmt_mechanisms.xlsx")


def null_test_fetch_gcmt():
    dataframe = fetch_gcmt()
    first = dataframe.iloc[0]
    assert first["time"] == datetime(1976, 1, 1, 1, 29, 39, 600000)
    assert first["lat"] == -28.61
    print(first["mrr"])
    assert first["mrr"] == 7.68e26
    random = dataframe.iloc[40000]
    assert random["time"] == datetime(2012, 11, 23, 0, 40, 21, 199999)
    assert random["lat"] == 1.62
    print(random["mrr"])
    assert random["mrr"] == 8.01e22


def test_ndk_read():
    homedir = pathlib.Path(__file__).parent  # where is this script?
    ndkfile = homedir / ".." / "data" / "test.ndk"
    dataframe = ndk_to_dataframe(ndkfile)
    assert dataframe.iloc[0]["time"] == datetime(2017, 1, 1, 14, 12, 8, 99999)
    assert dataframe.iloc[0]["lat"] == 3.66
    assert dataframe.iloc[0]["mrr"] == 2.460000e24


if __name__ == "__main__":
    # throw_away()
    test_ndk_read()
    # test_fetch_gcmt()
