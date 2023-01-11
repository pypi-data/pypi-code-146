import os

import pytest
from matplotlib import animation

import ct_analyser.cta as cta
from matplotlib import animation

# Testing the cta module.

# Test the load_example function.
@pytest.mark.parametrize("single_image",[True, False])
def test_load_example(single_image):
    example = cta.load_example(single_image)
    assert isinstance(example, cta.Scan)


@pytest.mark.parametrize("single_image, expected",
                        [(True, (512,512)),
                        (False, (64,512,512))])
def test_load_example_size(single_image, expected):
    example = cta.load_example(single_image)
    assert example.scan.shape == expected


# Define a fixture to load the example scan.
@pytest.fixture
def example():
    return cta.load_example(False)
# Define a fixture to load the example scan as a single image.
@pytest.fixture
def example_single():
    return cta.load_example(single_image=True)


# Test the import_dicom function.
def test_import_dicom(example):
    path = example.path
    dicom = cta.import_dicom(path)
    assert isinstance(dicom, cta.Scan)

# Test the import_dicom function with a single image.
def test_import_dicom_single(example_single):
    path = os.path.join(example_single.path, example_single.filenames)
    dicom = cta.import_dicom(path)
    assert isinstance(dicom, cta.Scan)

# Test the import_dicom function returns a scan of the correct shape.
def test_import_dicom_size(example):
    path = os.path.join(example.path)
    dicom = cta.import_dicom(path)
    assert dicom.scan.shape == (64, 512,512)

# Test the import_dicom function returns a scan of the correct shape 
# with a single image.
def test_import_dicom_single_size(example_single):
    path = os.path.join(example_single.path, example_single.filenames)
    dicom = cta.import_dicom(path)
    assert dicom.scan.shape == (512,512)

# Test display_scan function.
def test_display_scan(example):
    ani = cta.display_scan(example, 'off')
    assert isinstance(ani, animation.ArtistAnimation)

# Test display_scan function with a single image.
def test_display_scan_single(example_single):
    ani = cta.display_scan(example_single, 'off')
    assert ani == None

