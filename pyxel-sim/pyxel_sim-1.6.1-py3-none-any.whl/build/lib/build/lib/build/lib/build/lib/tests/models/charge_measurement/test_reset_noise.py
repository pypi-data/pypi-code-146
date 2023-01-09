#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Reset noise model tests."""

from typing import Optional

import pytest

from pyxel.detectors import (
    APD,
    CCD,
    APDCharacteristics,
    APDGeometry,
    CCDCharacteristics,
    CCDGeometry,
    Environment,
)
from pyxel.models.charge_measurement import ktc_noise


@pytest.fixture
def ccd_5x5() -> CCD:
    """Create a valid CCD detector."""
    return CCD(
        geometry=CCDGeometry(
            row=5,
            col=5,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(temperature=273.0),
        characteristics=CCDCharacteristics(
            adc_voltage_range=(0.0, 10.0),
        ),
    )


@pytest.fixture
def apd_5x5() -> APD:
    """Create a valid CCD detector."""
    return APD(
        geometry=APDGeometry(
            row=5,
            col=5,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(temperature=273.0),
        characteristics=APDCharacteristics(
            quantum_efficiency=1.0,
            adc_voltage_range=(0.0, 10.0),
            adc_bit_resolution=16,
            full_well_capacity=100000,
            avalanche_gain=1.0,
            pixel_reset_voltage=5.0,
            roic_gain=0.8,
        ),
    )


def test_ktc_noise(
    ccd_5x5: CCD,
    apd_5x5: APD,
):
    """Test model 'ktc_noise' with valid inputs."""
    ktc_noise(detector=ccd_5x5, node_capacitance=30.0e-15)
    ktc_noise(detector=apd_5x5, node_capacitance=None)


@pytest.mark.parametrize(
    "node_capacitance, exp_exc, exp_error",
    [
        pytest.param(
            -30e-15,
            ValueError,
            "Node capacitance should be larger than 0!",
        ),
        pytest.param(
            None,
            AttributeError,
            "Characteristic node_capacitance not available for the detector used. "
            "Please specify node_capacitance in the model argument!",
        ),
    ],
)
def test_ktc_noise_invalid(
    ccd_5x5: CCD, node_capacitance: Optional[float], exp_exc, exp_error
):
    """Test model 'output_pixel_reset_voltage_apd' with valid inputs."""
    detector = ccd_5x5
    with pytest.raises(exp_exc, match=exp_error):
        ktc_noise(detector=detector, node_capacitance=node_capacitance)
