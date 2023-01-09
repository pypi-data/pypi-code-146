#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.


import numpy as np
import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.readout_electronics import sar_adc_with_noise


@pytest.fixture
def ccd_10x3() -> CCD:
    """Create a valid CCD detector."""
    return CCD(
        geometry=CCDGeometry(
            row=10,
            col=3,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(
            adc_bit_resolution=8, adc_voltage_range=(0.0, 10.0)
        ),
    )


@pytest.mark.parametrize(
    "strengths, noises",
    [
        pytest.param(
            [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], id="list only 0"
        ),
        pytest.param(
            np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=float),
            np.array([0, 0, 0, 0, 0, 0, 0, 0], dtype=float),
            id="array only 0.0",
        ),
        pytest.param(
            [10, 20, 30, 40, 50, 60, 70, 80], [1, 2, 3, 4, 5, 6, 7, 8], id="list"
        ),
    ],
)
def test_sar_adc_with_noise(ccd_10x3: CCD, strengths, noises):
    """Test model 'sar_adc_with_noise' with valid inputs."""
    sar_adc_with_noise(detector=ccd_10x3, strengths=strengths, noises=noises)


@pytest.mark.parametrize(
    "strengths, noises, exp_error, exp_msg",
    [
        pytest.param(
            [],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ValueError,
            "parameter 'strengths'",
            id="No 'strengths",
        ),
        pytest.param(
            [0, 0, 0, 0, 0, 0, 0, 0],
            [],
            ValueError,
            "parameter 'noises'",
            id="No 'noises",
        ),
        pytest.param(
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ValueError,
            "parameter 'strengths'",
            id="Missing one 'strength",
        ),
        pytest.param(
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            ValueError,
            "parameter 'noises'",
            id="Missing one 'noise",
        ),
        pytest.param(
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ValueError,
            "parameter 'strengths'",
            id="Extra 'strength",
        ),
        pytest.param(
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ValueError,
            "parameter 'noises'",
            id="Extra 'noise",
        ),
    ],
)
def test_sar_adc_with_noise_invalid_params(
    ccd_10x3: CCD, strengths, noises, exp_error, exp_msg
):
    """Test model 'sar_adc_with_noise' with invalid inputs."""
    with pytest.raises(exp_error, match=exp_msg):
        sar_adc_with_noise(detector=ccd_10x3, strengths=strengths, noises=noises)
