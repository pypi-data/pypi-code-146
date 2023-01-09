#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.


from pathlib import Path

import numpy as np
import pytest

from pyxel.detectors import (
    CCD,
    CCDCharacteristics,
    CCDGeometry,
    Detector,
    Environment,
    ReadoutProperties,
)
from pyxel.models.charge_generation import load_charge


@pytest.fixture
def ccd_10x1() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=10,
            col=1,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


@pytest.fixture
def profile_10x1() -> np.ndarray:
    """Create a profile of 10x1."""
    data_1d = np.array([100, 100, 100, 100, 100, 0, 0, 0, 0, 0])

    return data_1d


@pytest.fixture
def profile_10x1_txt_filename(profile_10x1: np.ndarray, tmp_path: Path) -> Path:
    """Create a filename with a profile of 10x1."""
    filename = tmp_path / "profile_10x1.txt"
    np.savetxt(fname=filename, X=profile_10x1)

    return filename


@pytest.fixture
def ccd_10x3() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=10,
            col=3,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


@pytest.fixture
def profile_10x3() -> np.ndarray:
    """Create a profile of 10x3."""
    data_2d = np.zeros(shape=(10, 3))
    data_2d[:5, 0] = 100
    data_2d[:5, 1] = 200
    data_2d[:5, 2] = 300

    data_2d = np.array(
        [
            [100, 200, 300],
            [100, 200, 300],
            [100, 200, 300],
            [100, 200, 300],
            [100, 200, 300],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )

    return data_2d


@pytest.fixture
def profile_10x3_txt_filename(profile_10x3: np.ndarray, tmp_path: Path) -> Path:
    """Create a filename with a profile of 10x3."""
    filename = tmp_path / "profile_10x3.txt"
    np.savetxt(fname=filename, X=profile_10x3)

    return filename


def test_charge_profile_10x1(ccd_10x1: CCD, profile_10x1_txt_filename: Path) -> None:
    """Test function 'charge_profile'."""
    detector: Detector = ccd_10x1

    # Check initial detector object
    assert detector.geometry.row == 10
    assert detector.geometry.col == 1
    assert detector.charge.frame.empty

    # Run model
    load_charge(
        detector=detector,
        filename=profile_10x1_txt_filename,
    )

    # Check modified charges in 'detector'
    exp_charges = np.array([[100], [100], [100], [100], [100], [0], [0], [0], [0], [0]])
    charges = detector.charge.array

    np.testing.assert_array_almost_equal(charges, exp_charges)


def test_charge_profile_10x3(ccd_10x3: CCD, profile_10x3_txt_filename: Path) -> None:
    """Test function 'charge_profile'."""
    detector: Detector = ccd_10x3

    # Check initial detector object
    assert detector.geometry.row == 10
    assert detector.geometry.col == 3
    assert detector.charge.frame.empty

    # Run model
    load_charge(
        detector=detector,
        filename=profile_10x3_txt_filename,
    )

    # Check modified charges in 'detector'
    exp_charges = np.array(
        [
            [100, 200, 300],
            [100, 200, 300],
            [100, 200, 300],
            [100, 200, 300],
            [100, 200, 300],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
    )
    charges = detector.charge.array

    np.testing.assert_array_almost_equal(charges, exp_charges)
