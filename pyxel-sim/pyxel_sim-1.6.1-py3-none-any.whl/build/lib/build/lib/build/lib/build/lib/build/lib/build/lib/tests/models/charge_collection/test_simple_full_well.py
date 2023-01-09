#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Tests for full well models."""

import numpy as np
import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.charge_collection import simple_full_well


@pytest.fixture
def ccd_10x10() -> CCD:
    """Create a valid CCD detector."""
    return CCD(
        geometry=CCDGeometry(
            row=10,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )


@pytest.mark.parametrize(
    "fwc",
    [
        pytest.param(
            10,
        ),
        pytest.param(
            None,
        ),
    ],
)
def test_full_well(
    ccd_10x10: CCD,
    fwc: int,
):
    """Test model 'simple_full_well' with valid inputs."""

    detector = ccd_10x10
    detector.characteristics.full_well_capacity = 10
    detector.pixel.array = np.ones((detector.geometry.row, detector.geometry.col)) * 50

    simple_full_well(detector=ccd_10x10, fwc=fwc)

    assert np.max(detector.pixel.array <= 10)


@pytest.mark.parametrize(
    "fwc, exp_exc, exp_error",
    [
        pytest.param(
            -5,
            ValueError,
            "Full well capacity should be a positive number.",
        ),
    ],
)
def test_full_well_bad_inputs(
    ccd_10x10: CCD,
    fwc: int,
    exp_exc,
    exp_error,
):
    """Test model 'simple_full_well' with bad inputs."""
    with pytest.raises(exp_exc, match=exp_error):
        simple_full_well(detector=ccd_10x10, fwc=fwc)
