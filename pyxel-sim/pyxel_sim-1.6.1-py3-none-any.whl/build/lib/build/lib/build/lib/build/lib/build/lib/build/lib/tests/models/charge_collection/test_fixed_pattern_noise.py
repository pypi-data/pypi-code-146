from pathlib import Path
from typing import Union

import numpy as np
import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.charge_collection import fixed_pattern_noise
from pyxel.models.charge_collection.fixed_pattern_noise import compute_simple_prnu


@pytest.fixture
def ccd_5x5() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=5,
            col=5,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(quantum_efficiency=0.9),
    )
    return detector


@pytest.fixture
def valid_noise_path(
    tmp_path: Path,
) -> str:
    """Create valid 2D file on a temporary folder."""
    data_2d = (
        np.array(
            [
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
            ]
        )
        * 0.5
    )

    final_path = f"{tmp_path}/noise.npy"
    np.save(final_path, arr=data_2d)

    return final_path


def test_fixed_pattern_noise_valid_path(
    ccd_5x5: CCD, valid_noise_path: Union[str, Path]
):
    """Test function fixed_pattern_noise with valid path inputs."""

    detector = ccd_5x5

    array = np.ones((5, 5))
    detector.pixel.array = array
    target = array * 0.5

    fixed_pattern_noise(detector=detector, filename=valid_noise_path)

    np.testing.assert_array_almost_equal(detector.pixel.array, target)


def test_compute_simple_prnu(ccd_5x5: CCD):
    """Test function 'compute_simple_prnu'."""
    detector = ccd_5x5
    shape = detector.geometry.shape
    quantum_efficiency = detector.characteristics.quantum_efficiency
    fixed_pattern_noise_factor = 0.01

    prnu_2d = compute_simple_prnu(shape, quantum_efficiency, fixed_pattern_noise_factor)
    np.testing.assert_equal(prnu_2d.shape, shape)
    assert np.all(prnu_2d >= quantum_efficiency)


def test_fixed_pattern_noise_valid(ccd_5x5: CCD):
    """Test model fixed_pattern_noise with valid fpn inputs."""
    detector = ccd_5x5
    fixed_pattern_noise(detector=detector, fixed_pattern_noise_factor=0.01)


def test_fpn_raises(ccd_5x5: CCD, valid_noise_path: Union[str, Path]):
    """Test model fixed_pattern_noise when generating an error."""
    detector = ccd_5x5
    invalid_noise_path = "noise.npy"
    with pytest.raises(ValueError, match="filename or fixed_pattern_noise_factor"):
        fixed_pattern_noise(
            detector=detector,
            filename=valid_noise_path,
            fixed_pattern_noise_factor=0.01,
        )
    with pytest.raises(ValueError, match="filename or fixed_pattern_noise_factor"):
        fixed_pattern_noise(detector=detector)

    with pytest.raises(FileNotFoundError, match="Cannot find folder"):
        fixed_pattern_noise(detector=detector, filename=invalid_noise_path)
