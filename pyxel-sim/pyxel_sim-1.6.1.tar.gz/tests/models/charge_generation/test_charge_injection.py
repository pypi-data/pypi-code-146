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
"""Tests for charge injection models."""

import numpy as np
import pytest

from pyxel.detectors import (
    CCD,
    CMOS,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
)
from pyxel.models.charge_generation import charge_blocks


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


def test_charge_blocks_valid(ccd_10x10: CCD):
    """Test model 'charge_blocks' with valid inputs."""

    detector = ccd_10x10
    output = np.array(
        [
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        ]
    )

    charge_blocks(detector=detector, charge_level=1, block_start=0, block_end=5)

    np.testing.assert_array_almost_equal(output, detector.charge.array)


@pytest.mark.parametrize(
    "charge_level, block_start, block_end, exp_exc, exp_error",
    [
        pytest.param(
            1,
            0,
            15,
            ValueError,
            "Block end not in range of the detector shape.",
        ),
        pytest.param(
            1,
            -4,
            5,
            ValueError,
            "Block start not in range of the detector shape.",
        ),
        pytest.param(
            -1,
            0,
            5,
            ValueError,
            "Charge level value should not be a negative number.",
        ),
    ],
)
def test_charge_blocks_inputs(
    ccd_10x10: CCD,
    charge_level: int,
    block_start: int,
    block_end: int,
    exp_exc,
    exp_error,
):
    """Test model 'charge_blocks' with bad inputs."""
    with pytest.raises(exp_exc, match=exp_error):
        charge_blocks(
            detector=ccd_10x10,
            charge_level=charge_level,
            block_start=block_start,
            block_end=block_end,
        )


def test_charge_blocks_with_cmos():
    """Test model 'charge_blocks' with a `CMOS` detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=5,
            col=4,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CMOSCharacteristics(),
    )

    with pytest.raises(TypeError, match="Expecting a CCD object for detector."):
        charge_blocks(detector=detector, charge_level=1)
