#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.


from typing import Union

import pytest

from pyxel.detectors import (
    APD,
    CCD,
    CMOS,
    APDCharacteristics,
    APDGeometry,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
)
from pyxel.models.charge_measurement import (
    output_node_noise,
    output_node_noise_cmos,
    readout_noise_saphira,
)


@pytest.fixture
def ccd_5x10() -> CCD:
    """Create a valid CCD detector."""
    return CCD(
        geometry=CCDGeometry(
            row=5,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )


@pytest.fixture
def cmos_5x10() -> CMOS:
    """Create a valid CMOS detector."""
    return CMOS(
        geometry=CMOSGeometry(
            row=5,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CMOSCharacteristics(charge_to_volt_conversion=1.0e-6),
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
        environment=Environment(),
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


@pytest.mark.parametrize("detector_type", ["ccd", "cmos"])
@pytest.mark.parametrize(
    "std_deviation",
    [pytest.param(1.0, id="std positive"), pytest.param(0.0, id="std null")],
)
def test_output_node_noise(
    ccd_5x10: CCD,
    cmos_5x10: CMOS,
    detector_type: str,
    std_deviation: float,
):
    """Test model 'output_node_noise' with valid inputs."""
    if detector_type == "ccd":
        detector: Union[CCD, CMOS] = ccd_5x10
    elif detector_type == "cmos":
        detector = cmos_5x10
    else:
        raise NotImplementedError

    output_node_noise(detector=detector, std_deviation=std_deviation)


@pytest.mark.parametrize("detector_type", ["ccd", "cmos"])
def test_output_node_noise_bad_std(ccd_5x10: CCD, cmos_5x10: CMOS, detector_type: str):
    """Test model 'output_node_noise' with invalid input(s)."""
    if detector_type == "ccd":
        detector: Union[CCD, CMOS] = ccd_5x10
    elif detector_type == "cmos":
        detector = cmos_5x10
    else:
        raise NotImplementedError

    with pytest.raises(ValueError, match="'std_deviation' must be positive."):
        output_node_noise(detector=detector, std_deviation=-1.0)


def test_output_node_noise_cmos(cmos_5x10: CMOS):
    """Test model 'output_node_noise_cmos' with valid inputs."""
    detector = cmos_5x10

    output_node_noise_cmos(detector=detector, readout_noise=1.0, readout_noise_std=0.1)


def test_output_node_noise_with_ccd(ccd_5x10: CCD):
    """Test model 'output_node_noise_ccd' with a 'CCD'."""
    detector = ccd_5x10

    with pytest.raises(TypeError, match="Expecting a 'CMOS' detector object."):
        output_node_noise_cmos(
            detector=detector, readout_noise=1.0, readout_noise_std=2.0
        )


def test_output_node_noise_invalid_noise(cmos_5x10: CMOS):
    """Test model 'output_node_noise_ccd' with a 'CCD'."""
    detector = cmos_5x10

    with pytest.raises(ValueError, match="'readout_noise_std' must be positive."):
        output_node_noise_cmos(
            detector=detector, readout_noise=1.0, readout_noise_std=-1.0
        )


def test_readout_noise_saphira_with_ccd(ccd_5x10: CCD):
    """Test model 'readout_noise_saphira' with a 'CCD'."""
    detector = ccd_5x10

    with pytest.raises(TypeError, match="Expecting a 'APD' detector object."):
        readout_noise_saphira(
            detector=detector, roic_readout_noise=0.1, controller_noise=0.1
        )


def test_readout_noise_saphira(apd_5x5: APD):
    """Test model 'readout_noise_saphira' with valid inputs."""
    detector = apd_5x5

    readout_noise_saphira(
        detector=detector, roic_readout_noise=0.1, controller_noise=0.1
    )
