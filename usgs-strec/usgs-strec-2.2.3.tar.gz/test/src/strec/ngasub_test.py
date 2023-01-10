#!/usr/bin/env python

# stdlib imports
import pathlib

# third party imports
import numpy as np
import pandas as pd
from esi_utils_rupture.tensor import fill_tensor_from_angles

# local imports
from strec.ngasub import nga_categorize
from strec.subtype import SubductionSelector


def test_nga_categorize():
    datafile = pathlib.Path(__file__).parent / "data" / "big_focals.xlsx"
    dataframe = pd.read_excel(datafile)
    dataframe = dataframe.drop_duplicates(subset=["EventID"])
    subset_file = pathlib.Path(__file__).parent / "data" / "subsampled_nga_results.xlsx"
    subset = pd.read_excel(subset_file)
    idx = dataframe["EventID"].isin(subset["EventID"])
    dataframe = dataframe.loc[idx]
    subset = subset.sort_values(by="EventID")
    dataframe = dataframe.sort_values(by="EventID")
    selector = SubductionSelector(verbose=False, prefix="")
    results = []
    ic = 0
    for idx, row in dataframe.iterrows():
        # event_id = row["comcat_id"]
        # detail = get_event_details(event_id)
        # lat, lon, depth = detail["latitude"], detail["longitude"], detail["depth"]
        lat = row["EventLatitude"]
        lon = row["EventLongitude"]
        depth = row["EventDepth"]
        strike = row["NodalPlane1Strike"]
        dip = row["NodalPlane1Dip"]
        rake = row["NodalPlane1Rake"]
        eventid = row["EventID"]
        mag = row["EventMagnitude"]
        tensor_params = None
        if not np.isnan(strike):
            tensor_params = fill_tensor_from_angles(strike, dip, rake, mag)
        strec_info = selector.getSubductionType(
            lat,
            lon,
            depth,
            eventid=eventid,
            tensor_params=tensor_params,
        )
        nga_strec_info = nga_categorize([lat, lon, depth], strec_info)
        nga_strec_info["EventID"] = eventid
        results.append(nga_strec_info)
        ic += 1
        print(f"Processed event {ic} of {len(dataframe)} events.")
    results_frame = pd.DataFrame(results)
    assert results_frame["NGACategory"].equals(subset["NGACategory"])


if __name__ == "__main__":
    test_nga_categorize()
