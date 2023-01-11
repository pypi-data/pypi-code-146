import pytest
import numpy as np

import ct_analyser.cta as cta
import ct_analyser.mask as mask

# Testing the isolate_pt function and masked scan object.

# Define a fixture to load the example scans.
@pytest.fixture
def example():
    return cta.load_example(single_image=False)

@pytest.fixture
def example_single():
    return cta.load_example(single_image=True)

# Test isolate patient function returns MaskedScan object.
@pytest.mark.parametrize("scan", ["example_single", "example"])
@pytest.mark.parametrize("median_filter", [True, False])
def test_isolate_patient(scan,median_filter, request):
    scan_obj = request.getfixturevalue(scan)
    mask_scan = mask.isolate_pt(scan_obj, med_filter=median_filter)
    assert isinstance(mask_scan, cta.MaskedScan)

# Get masked scan object.
@pytest.fixture
def masked_scan(request):
    scan_obj = request.getfixturevalue("example")
    return mask.isolate_pt(scan_obj,med_filter=False)

@pytest.fixture
def masked_scan_single(request):
    scan_obj = request.getfixturevalue("example_single")
    return mask.isolate_pt(scan_obj,med_filter=False)

# Test that the masked scan contains a mask of the type numpy.ndarray.
@pytest.mark.parametrize("scan", ["masked_scan_single", "masked_scan"])
def test_masked_scan_type(scan, request):
    masked_scan = request.getfixturevalue(scan)
    assert isinstance(masked_scan.mask, np.ndarray)

# Test that the masked scan contains a masked image of the correct 
# shape.
@pytest.mark.parametrize("scan, shape", 
                        [("masked_scan_single",(512,512)), 
                        ("masked_scan", (64,512,512))])
def test_masked_scan_shape(scan, shape, request):
    masked_scan = request.getfixturevalue(scan)
    assert masked_scan.masked_scan.shape == shape

