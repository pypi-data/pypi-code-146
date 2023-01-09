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


@pytest.fixture
def environment() -> Environment:
    return Environment()


@pytest.fixture
def ccd_geometry() -> CCDGeometry:
    return CCDGeometry(row=1, col=1)


@pytest.fixture
def ccd_characteristics() -> CCDCharacteristics:
    return CCDCharacteristics()


@pytest.fixture
def CCD_empty(ccd_geometry, environment, ccd_characteristics) -> CCD:
    detector = CCD(
        geometry=ccd_geometry,
        environment=environment,
        characteristics=ccd_characteristics,
    )
    return detector


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
        environment=Environment(temperature=200.0),
        characteristics=CCDCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector
