#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import numpy as np
import pytest

from pyxel.detectors import (
    CCD,
    CMOS,
    MKID,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
    MKIDCharacteristics,
    MKIDGeometry,
)
from pyxel.models.readout_electronics import dead_time_filter
from pyxel.models.readout_electronics.dead_time import apply_dead_time_filter


@pytest.fixture
def mkid_5x4() -> MKID:
    """Create a valid CCD detector."""
    detector = MKID(
        geometry=MKIDGeometry(
            row=5,
            col=4,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=MKIDCharacteristics(),
    )

    detector.reset()

    return detector


def test_apply_dead_time_filter():
    """Test function 'apply_dead_time_filter."""
    data_2d = np.array(
        [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 13, 14],
            [15, 16, 17, 18, 19],
        ]
    )

    result_2d = apply_dead_time_filter(phase_2d=data_2d, maximum_count=12)

    exp_data_2d = np.array(
        [
            [0, 1, 2, 3, 4],
            [5, 6, 7, 8, 9],
            [10, 11, 12, 12, 12],
            [12, 12, 12, 12, 12],
        ]
    )

    np.testing.assert_equal(result_2d, exp_data_2d)


@pytest.mark.parametrize("dead_time", [1.0, 2])
def test_dead_time_filter(mkid_5x4: MKID, dead_time: float):
    """Test function 'dead_time_filter'."""
    dead_time_filter(detector=mkid_5x4)


def test_dead_time_filter_with_ccd():
    """Test model 'dead_time_filter' with a `CCD` detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=5,
            col=4,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )

    with pytest.raises(TypeError, match=r"Expecting an `MKID` object for 'detector'"):
        dead_time_filter(detector=detector)


def test_dead_time_filter_with_cmos():
    """Test model 'dead_time_filter' with a `CMOS` detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=5,
            col=4,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CMOSCharacteristics(),
    )

    with pytest.raises(TypeError, match=r"Expecting an `MKID` object for 'detector'"):
        dead_time_filter(detector=detector)
