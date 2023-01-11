import pytest
import numpy as np
import pandas as pd

import ct_analyser.cta as cta
import ct_analyser.mask as mask
import ct_analyser.segment as segment

# Test contour, heart isolate and lung body isolate functions.

# Define a fixture to load the example scans as Scan objects.
@pytest.fixture
def example():
    return cta.load_example(single_image=False)


@pytest.fixture
def example_single():
    return cta.load_example(single_image=True)

# Define a fixture to load the example scans and return MaskedScan. 
# object.
@pytest.fixture
def example_mask():
    scan = cta.load_example(single_image=False)
    return mask.isolate_pt(scan, med_filter=False)

# Define a fixture to load a single image example scan and return MaskedScan .
@pytest.fixture
def example_single_mask():
    scan = cta.load_example(single_image=True)
    return mask.isolate_pt(scan, med_filter=False)

# Modify the scan object to have a smaller, dummy scan. Allows for the
# test to run faster.
@pytest.fixture
def dummy_scan(example):
    example2 = example
    example2.scan = example2.scan[36:38]
    return example2

@pytest.fixture
def dummy_mask(example_mask):
    example2 = example_mask
    example2.masked_scan = example2.masked_scan[36:38]
    example2.mask = example2.mask[36:38]
    example2.scan = example2.scan[36:38]
    return example2

# Test the contour function return types
@pytest.mark.parametrize("scan, type, slice_no",
                        [("example_single_mask", segment.ContouredScan,
                        32),
                        ("dummy_mask", segment.ContouredScan, 0),
                        ("example_single", segment.ContouredScan, 32),
                        ("dummy_scan", segment.ContouredScan, 0)])
def test_contour_type(scan, type, slice_no, request):
    masked_scan = request.getfixturevalue(scan)
    contour = segment.contour(masked_scan, True, slice_no = slice_no) 
    assert isinstance(contour, type)

# Test lung body isolate function return types
@pytest.mark.parametrize("scan, type",
                        [("example_single_mask", segment.ContouredScan),
                        ("dummy_mask", segment.ContouredScan),
                        ("example_single", segment.ContouredScan),
                        ("dummy_scan", segment.ContouredScan)])
def test_lung_body_isolate(scan, type, request):
    image = request.getfixturevalue(scan)
    masked_arr, lung_body = segment.lung_body_isolate(image, True)
    assert all([isinstance(masked_arr, np.ndarray),
                isinstance(lung_body, type)])



# Test heart isolate function return types
@pytest.mark.parametrize("scan, ind, loc2",
                        [("example_single_mask",np.array((0,0)), None),
                        ("dummy_mask",np.array((0,2)), np.array((286, 258))),
                        ("example_single",np.array((0,0)), None),
                        ("dummy_scan",np.array((0,2)), np.array((286, 258)))])
def test_heart_isolate(scan, ind, loc2, request):
    image = request.getfixturevalue(scan)
    heart_info = {
                    "Index": ind,
                    "Primary ROI": np.array((285, 260)),
                    "Secondary ROI": loc2,
                    "Radius": 75
                    }
    masked_arr, contour = segment.heart_isolate(image, heart_info, True)
    assert all([isinstance(masked_arr, np.ndarray),
                isinstance(contour, segment.ContouredScan)])

# Test heart isolate function return types when input is an array
@pytest.mark.parametrize("scan",
                        ["example_single",
                        "dummy_scan"])
def test_heart_isolate_arr_input(scan, request):
    heart_info = {
    "Index": np.array((0,2)),
    "Primary ROI": np.array((285, 260)),
    "Secondary ROI": np.array((286, 258)),
    "Radius": 75
    }
    image = request.getfixturevalue(scan).scan
    masked_arr, df = segment.heart_isolate(image, heart_info, True)
    assert all([isinstance(masked_arr, np.ndarray),
                isinstance(df, pd.core.frame.DataFrame)])