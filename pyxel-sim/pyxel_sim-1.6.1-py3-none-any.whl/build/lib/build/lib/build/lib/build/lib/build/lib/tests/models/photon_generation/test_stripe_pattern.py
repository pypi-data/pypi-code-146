#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#

#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
import pytest

from pyxel.detectors import (
    CCD,
    CCDCharacteristics,
    CCDGeometry,
    Environment,
    ReadoutProperties,
)
from pyxel.models.photon_generation import stripe_pattern


@pytest.fixture
def ccd_20x20() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=20,
            col=20,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


@pytest.mark.parametrize(
    "period, level, angle, startwith, time_scale",
    [
        pytest.param(
            2,
            10.0,
            0,
            0,
            1.0,
            id="valid",
        ),
        pytest.param(
            1,
            10.0,
            0,
            0,
            1.0,
            id="period_too_small",
            marks=pytest.mark.xfail(raises=ValueError, strict=True),
        ),
        pytest.param(
            5,
            10.0,
            0,
            0,
            1.0,
            id="period_not_multiple_of_2",
            marks=pytest.mark.xfail(raises=ValueError, strict=True),
        ),
    ],
)
def test_stripe_pattern(
    ccd_20x20: CCD,
    period: int,
    level: float,
    angle: int,
    startwith: int,
    time_scale: float,
):
    """Test input parameters for function 'stripe_pattern'."""

    stripe_pattern(
        detector=ccd_20x20,
        period=period,
        level=level,
        angle=angle,
        startwith=startwith,
        time_scale=time_scale,
    )
