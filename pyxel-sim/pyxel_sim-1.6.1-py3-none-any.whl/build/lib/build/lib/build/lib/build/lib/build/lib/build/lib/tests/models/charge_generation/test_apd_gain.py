#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
import numpy as np
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
from pyxel.models.charge_generation import apd_gain


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
            avalanche_gain=2.0,
            pixel_reset_voltage=5.0,
            roic_gain=0.8,
        ),
    )


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
        environment=Environment(),
        characteristics=CCDCharacteristics(
            adc_voltage_range=(0.0, 10.0),
        ),
    )


def test_apd_gain_invalid_detector(ccd_5x5: CCD):
    """Test model 'apd_gain' with a 'CCD'."""
    detector = ccd_5x5

    with pytest.raises(TypeError, match="Expecting a 'APD' detector object."):
        apd_gain(detector=detector)


def test_apd_gain(apd_5x5: APD):
    """Test model 'apd_gain' with a 'APD'."""
    detector = apd_5x5

    detector.charge.add_charge_array(array=np.ones((5, 5)))

    apd_gain(detector=detector)

    detector.charge.add_charge(
        particle_type="e",
        particles_per_cluster=np.array([1.0]),
        init_energy=np.array([0]),
        init_ver_position=np.array([0]),
        init_hor_position=np.array([0]),
        init_z_position=np.array([0]),
        init_ver_velocity=np.array([0]),
        init_hor_velocity=np.array([0]),
        init_z_velocity=np.array([0]),
    )

    assert detector.charge.frame_empty() is False

    apd_gain(detector=detector)
