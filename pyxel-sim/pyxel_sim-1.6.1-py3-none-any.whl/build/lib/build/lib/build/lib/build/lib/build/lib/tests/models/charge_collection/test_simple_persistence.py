#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

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
from pyxel.models.charge_collection import simple_persistence


@pytest.fixture
def cmos_5x10() -> CMOS:
    """Create a valid CCD detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=5,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CMOSCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)

    return detector


@pytest.fixture
def ccd_5x5() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
        geometry=CCDGeometry(
            row=5,
            col=5,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CCDCharacteristics(),
    )
    return detector


def test_simple_persistence_two_traps(cmos_5x10: CMOS):
    """Test model 'simple_persistence'."""
    detector = cmos_5x10

    # No persistence
    assert not detector.has_persistence()

    simple_persistence(
        detector=detector,
        trap_time_constants=[1.0, 3.0],
        trap_densities=[0.1, 0.1],
    )

    assert detector.has_persistence()
    assert len(detector.persistence.trap_list) == 2


def test_simple_persistence_one_trap(cmos_5x10: CMOS):
    """Test model 'simple_persistence'."""
    detector = cmos_5x10

    # No persistence
    assert not detector.has_persistence()

    # With persistence
    simple_persistence(
        detector=detector,
        trap_time_constants=[1.0],
        trap_densities=[0.1],
    )

    assert detector.has_persistence()
    assert len(detector.persistence.trap_list) == 1


@pytest.mark.parametrize(
    "trap_time_constants, trap_densities, exp_error, exp_msg",
    [
        pytest.param(
            [],
            [],
            ValueError,
            "Expecting at least one 'trap_time_constants' and 'trap_densities'",
            id="no elements",
        ),
        pytest.param(
            [1.0],
            [0.1, 0.1],
            ValueError,
            "Expecting same number of elements for parameters",
            id="not same number of elements",
        ),
    ],
)
def test_simple_persistence_bad_inputs(
    cmos_5x10: CMOS,
    trap_time_constants,
    trap_densities,
    exp_error,
    exp_msg,
):
    """Test model 'simple_persistence' with bad inputs."""
    detector = cmos_5x10

    with pytest.raises(exp_error, match=exp_msg):
        simple_persistence(
            detector=detector,
            trap_time_constants=trap_time_constants,
            trap_densities=trap_densities,
        )


def test_persistence_with_ccd(ccd_5x5: CCD):
    """Test model 'simple_persistence' with a `CCD` detector."""
    with pytest.raises(TypeError, match="Expecting a CMOS object for detector."):
        detector = ccd_5x5

        simple_persistence(
            detector=detector,
            trap_time_constants=[1.0, 10.0],
            trap_densities=[0.1, 0.1],
        )
