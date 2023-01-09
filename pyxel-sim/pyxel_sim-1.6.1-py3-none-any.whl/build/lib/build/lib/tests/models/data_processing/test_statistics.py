#   Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#  #
#   This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#   is part of this Pyxel package. No part of the package, including
#   this file, may be copied, modified, propagated, or distributed except according to
#   the terms contained in the file ‘LICENCE.txt’.

import pytest

from pyxel.detectors import (
    CCD,
    CCDCharacteristics,
    CCDGeometry,
    Environment,
    ReadoutProperties,
)
from pyxel.models.data_processing import compute_statistics


@pytest.fixture
def ccd_10x10() -> CCD:
    """Create a valid CCD detector."""
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
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


def test_statistics(ccd_10x10: CCD):
    """Test input parameters for function 'statistics'."""
    detector = ccd_10x10
    compute_statistics(detector=detector)
    dataset = detector.processed_data.data
    assert "time" in dataset.coords
    assert list(dataset.coords["time"].values) == [0.0]
