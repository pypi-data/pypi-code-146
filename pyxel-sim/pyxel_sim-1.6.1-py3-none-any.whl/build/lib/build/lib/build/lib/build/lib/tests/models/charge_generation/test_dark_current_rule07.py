#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Tests for dark current models."""

import pytest

from pyxel.detectors import (
    CCD,
    CMOS,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
    ReadoutProperties,
)
from pyxel.models.charge_generation import dark_current_rule07


@pytest.fixture
def cmos_10x10() -> CMOS:
    """Create a valid CCD detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=10,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(temperature=273.15),
        characteristics=CMOSCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


def test_dark_current_rule07_valid(cmos_10x10: CMOS):
    """Test model 'dark_current_rule07' with valid inputs."""
    dark_current_rule07(
        detector=cmos_10x10,
    )


def test_dark_current_rule07_with_ccd():
    """Test model 'dark_current_rule07' with a `CCD` detector."""
    detector = CCD(
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

    with pytest.raises(TypeError, match="Expecting a CMOS object for detector."):
        dark_current_rule07(
            detector=detector,
        )
