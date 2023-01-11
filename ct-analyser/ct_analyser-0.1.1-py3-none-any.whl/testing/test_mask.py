import pytest
import numpy as np

import ct_analyser.cta as cta
import ct_analyser.mask as mask

# Test median filter, invert  and analyse functions.

# Define a fixture to load the example scans.
@pytest.fixture
def example():
    return cta.load_example(single_image=False)

# Define a fixture to load the example scans with a single image.
@pytest.fixture
def example_single():
    return cta.load_example(single_image=True)

# Get masked scan object.
@pytest.fixture
def masked_scan(request):
    scan_obj = request.getfixturevalue("example")
    return mask.isolate_pt(scan_obj,med_filter=False)

# Get masked scan object with a single image.
@pytest.fixture
def masked_scan_single(request):
    scan_obj = request.getfixturevalue("example_single")
    return mask.isolate_pt(scan_obj,med_filter=False)

# Test that the median filter function returns a numpy.ndarray.
@pytest.mark.parametrize("scan", ["masked_scan_single", "masked_scan"])
def test_median_filter(scan, request):
    image = request.getfixturevalue(scan).masked_scan
    filtered = mask.median_filter(image)
    assert isinstance(filtered, np.ndarray)

# Test that the median filter function returns an array of the correct shape.
@pytest.mark.parametrize("scan, shape",
                        [("masked_scan_single",(512,512)),
                        ("masked_scan", (64,512,512))])
def test_median_filter_shape(scan, shape, request):
    image = request.getfixturevalue(scan).masked_scan
    filtered = mask.median_filter(image)
    assert filtered.shape == shape

# Test that the invert function returns a numpy.ndarray.
@pytest.mark.parametrize("scan", ["masked_scan_single", "masked_scan"])
def test_invert(scan, request):
    masked_scan = request.getfixturevalue(scan)
    inverted = mask.invert(masked_scan.mask)
    assert isinstance(inverted, np.ndarray)

# Test that the invert function returns an array of the correct shape.
@pytest.mark.parametrize("scan, shape",
                        [("masked_scan_single",(512,512)),
                        ("masked_scan", (64,512,512))])
def test_invert_shape(scan, shape, request):
    masked_scan = request.getfixturevalue(scan)
    inverted = mask.invert(masked_scan.mask)
    assert inverted.shape == shape

#  Test that invert correctly inverts the mask.
def test_invert_correct():
    mask_array = np.array([[0,1,0],[1,0,1],[0,1,0]])
    inverted = mask.invert(mask_array)
    assert np.array_equal(inverted, np.array([[1,0,1],[0,1,0],[1,0,1]]))

# Test that the analyse function returns a dictionary.
@pytest.mark.parametrize("scan", ["masked_scan_single", "masked_scan"])
def test_analyse(scan, request):
    masked_scan = request.getfixturevalue(scan)
    analysis = mask.analyse(masked_scan)
    assert isinstance(analysis, dict)