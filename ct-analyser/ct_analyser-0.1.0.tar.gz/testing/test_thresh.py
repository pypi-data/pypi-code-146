import pytest
import numpy as np

import ct_analyser.cta as cta
import ct_analyser.mask as mask

# Testing the thresholding functions.

# Define a fixture to load the example scans.
@pytest.fixture
def example():
    return cta.load_example(single_image=False)

@pytest.fixture
def example_single():
    return cta.load_example(single_image=True)

# Test bimodal threshold function returns a numpy.ndarray.
@pytest.mark.parametrize("scan", ["example_single", "example"])
def test_bimodal_threshold_type(scan, request):
    scan_obj = request.getfixturevalue(scan)
    threshold = mask.bimodal_threshold(scan_obj)
    assert isinstance(threshold, np.ndarray)

# Test bimodal threshold function array is of the correct shape.
@pytest.mark.parametrize("scan, shape",
                        [("example", (64,512,512)),
                        ("example_single", (512,512))])
def test_bimodal_threshold_shape(scan, shape, request):
    scan_obj = request.getfixturevalue(scan)
    threshold = mask.bimodal_threshold(scan_obj)
    assert threshold.shape == shape

# Test bimodal threshold function array is is correctly masked.
@pytest.mark.parametrize("threshold, expected", [(None, 5),
                                                (3,4)])
def test_bimodal_threshold(threshold, expected):
    array = np.array([[x for x in range(10)] for y in range(10)])
    expected_arr = np.array([[0  if x < expected else 1 for x in range(10)] 
                                                for y in range(10)])
    threshold = mask.bimodal_threshold(array,threshold)
    assert np.array_equal(threshold, expected_arr)

# Test that mask threshold function returns a numpy.ndarray.
@pytest.mark.parametrize("scan", ["example_single", "example"])
def test_mask_threshold_type(scan, request):
    scan_obj = request.getfixturevalue(scan)
    threshold = mask.mask_threshold(scan_obj, 'Air')
    assert isinstance(threshold, np.ndarray)

# Test that mask threshold function array is of the correct shape.
@pytest.mark.parametrize("scan, shape",[("example", (64,512,512)),
                                        ("example_single", (512,512))])
def test_mask_threshold_shape(scan, shape, request):
    scan_obj = request.getfixturevalue(scan)
    threshold = mask.mask_threshold(scan_obj, 'Air')
    assert threshold.shape == shape

# Test that mask threshold function array is correctly masked.
@pytest.mark.parametrize("scan", ["example_single", "example"])
@pytest.mark.parametrize("threshold, min, max", 
                        [('Air', -2000, -801),
                        ('Lung', -800, -300),
                        ('Fat', -120, -60),
                        ('Fluid', -10, 20),
                        ('Soft Tissue', 21, 300),
                        ('Bone', 301, 1500),
                        ('Foreign Object', 1501, 30000)])
def test_mask_threshold(scan, threshold, min, max, request):
    scan_obj = request.getfixturevalue(scan)
    threshold = mask.mask_threshold(scan_obj, threshold)
    pixel_intesity = scan_obj.scan[np.where(threshold == 1)]
    assert np.all(pixel_intesity >= min) and np.all(pixel_intesity <= max)