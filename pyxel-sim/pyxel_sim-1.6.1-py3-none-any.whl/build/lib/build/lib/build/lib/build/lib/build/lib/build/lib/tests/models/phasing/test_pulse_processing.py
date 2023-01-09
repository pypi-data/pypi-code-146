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

"""Tests for pulse_processing model."""

import pytest

from pyxel.detectors import (
    CCD,
    MKID,
    CCDCharacteristics,
    CCDGeometry,
    Environment,
    MKIDCharacteristics,
    MKIDGeometry,
)
from pyxel.models.phasing import pulse_processing


@pytest.fixture
def mkid_5x5() -> MKID:
    """Create a valid MKID detector."""
    detector = MKID(
        geometry=MKIDGeometry(
            row=10,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=MKIDCharacteristics(),
    )
    return detector


@pytest.mark.parametrize(
    "wavelength, responsivity, scaling_factor",
    [
        pytest.param(
            1.0,
            1.0,
            1.0,
        ),
    ],
)
def test_pulse_processing_valid(
    mkid_5x5: MKID, wavelength: float, responsivity: float, scaling_factor: float
):
    """Test model 'pulse_processing' with valid inputs."""
    pulse_processing(
        detector=mkid_5x5,
        wavelength=wavelength,
        responsivity=responsivity,
        scaling_factor=scaling_factor,
    )


@pytest.mark.parametrize(
    "wavelength, responsivity, scaling_factor, exp_exc, exp_error",
    [
        pytest.param(
            -1.0,
            1.0,
            1.0,
            ValueError,
            "Only positive values accepted for wavelength.",
        ),
        pytest.param(
            1.0,
            1.0,
            -1.0,
            ValueError,
            "Only positive values accepted for scaling_factor.",
        ),
        pytest.param(
            1.0,
            -1.0,
            1.0,
            ValueError,
            "Only positive values accepted for responsivity.",
        ),
    ],
)
def test_pulse_processing_invalid(
    mkid_5x5: MKID,
    wavelength: float,
    responsivity: float,
    scaling_factor: float,
    exp_exc,
    exp_error,
):
    """Test model 'pulse_processing' with valid inputs."""
    with pytest.raises(exp_exc, match=exp_error):
        pulse_processing(
            detector=mkid_5x5,
            wavelength=wavelength,
            responsivity=responsivity,
            scaling_factor=scaling_factor,
        )


def test_pulse_processing_with_ccd():
    """Test model 'pulse_processing' with a `CCD` detector."""
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

    with pytest.raises(TypeError, match="Expecting a MKID object for the detector."):
        pulse_processing(
            detector=detector, wavelength=1.0, responsivity=1.0, scaling_factor=1.0
        )
