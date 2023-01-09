#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#

import pytest
from typing_extensions import Literal

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.readout_electronics import simple_adc


@pytest.fixture
def ccd_3x3() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=3,
            col=3,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(
            adc_bit_resolution=16, adc_voltage_range=(0.0, 10.0)
        ),
    )
    return detector


@pytest.mark.parametrize("data_type", ["uint16", "uint32", "uint64", "uint"])
def test_simple_adc(
    ccd_3x3: CCD, data_type: Literal["uint16", "uint32", "uint64", "uint"]
):
    """Test model 'simple_adc'."""
    simple_adc(detector=ccd_3x3, data_type=data_type)


@pytest.mark.parametrize(
    "data_type, exp_exc, exp_error",
    [
        ("float", TypeError, "Expecting a signed/unsigned integer"),
        ("float32", TypeError, "Expecting a signed/unsigned integer"),
        ("float64", TypeError, "Expecting a signed/unsigned integer"),
        ("uint8", TypeError, "Expected type of Image array is uint64"),
        ("int32", TypeError, "Expected type of Image array is uint64"),
        ("int64", TypeError, "Expected type of Image array is uint64"),
        ("int", TypeError, "Expected type of Image array is uint64"),
    ],
)
def test_simple_adc_wrong_data_type(
    ccd_3x3: CCD,
    data_type: str,
    exp_exc,
    exp_error,
):
    """Test model 'simple_adc' with wrong 'data_type'."""
    with pytest.raises(exp_exc, match=exp_error):
        simple_adc(
            detector=ccd_3x3,
            data_type=data_type,
        )
