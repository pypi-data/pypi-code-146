#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#

from typing import Sequence

import numpy as np
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
from pyxel.models.charge_measurement import (
    output_node_linearity_poly,
    physical_non_linearity,
    physical_non_linearity_with_saturation,
    simple_physical_non_linearity,
)


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
        environment=Environment(temperature=80),
        characteristics=CCDCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


@pytest.fixture
def cmos_5x5() -> CMOS:
    """Create a valid CMOS detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=5,
            col=5,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(temperature=80),
        characteristics=CMOSCharacteristics(),
    )
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


@pytest.mark.parametrize(
    "coefficients",
    [
        pytest.param([0, 1, 0.9]),
        pytest.param([5, 0.5, 0.9, 0.8]),
        pytest.param([3]),
        pytest.param([0, 3]),
    ],
)
def test_non_linearity_valid(ccd_5x5: CCD, coefficients: Sequence):
    """Test model 'non_linearity' with valid inputs."""
    detector = ccd_5x5
    detector.signal.array = np.ones(detector.signal.shape)
    output_node_linearity_poly(detector=detector, coefficients=coefficients)


@pytest.mark.parametrize(
    "coefficients, exp_exc, exp_error",
    [
        pytest.param(
            [], ValueError, "Length of coefficient list should be more than 0."
        ),
        pytest.param(
            [0, -1],
            ValueError,
            "Signal array contains negative values after applying non-linearity model!",
        ),
    ],
)
def test_non_linearity_invalid(
    ccd_5x5: CCD, coefficients: Sequence, exp_exc, exp_error
):
    """Test model 'non_linearity' with valid inputs."""
    detector = ccd_5x5
    detector.signal.array = np.ones(detector.signal.shape)
    with pytest.raises(exp_exc, match=exp_error):
        output_node_linearity_poly(detector=detector, coefficients=coefficients)


def test_simple_physical_non_linearity_valid(cmos_5x5: CMOS):
    """Test model 'simple_physical_non_linearity' with valid inputs."""
    detector = cmos_5x5
    detector.signal.array = np.ones(detector.signal.shape)
    simple_physical_non_linearity(
        detector=detector,
        cutoff=2.0,
        n_acceptor=1.0e18,
        n_donor=1.0e15,
        diode_diameter=5.0,
        v_bias=0.1,
    )


def test_physical_non_linearity_valid(cmos_5x5: CMOS):
    """Test model 'physical_non_linearity' with valid inputs."""
    detector = cmos_5x5
    detector.signal.array = np.ones(detector.signal.shape)
    physical_non_linearity(
        detector=detector,
        cutoff=2.0,
        n_acceptor=1.0e18,
        n_donor=1.0e15,
        diode_diameter=5.0,
        v_bias=0.1,
        fixed_capacitance=5.0e-15,
    )


def test_physical_non_linearity_with_saturation_valid(cmos_5x5: CMOS):
    """Test model 'physical_non_linearity_with_saturation' with valid inputs."""
    detector = cmos_5x5
    detector.signal.array = np.ones(detector.signal.shape)
    physical_non_linearity_with_saturation(
        detector=detector,
        cutoff=2.0,
        n_acceptor=1.0e18,
        n_donor=1.0e15,
        phi_implant=5.0,
        d_implant=2.0,
        saturation_current=0.001,
        ideality_factor=1.34,
        v_reset=0.0,
        d_sub=0.220,
        fixed_capacitance=5.0e-15,
        euler_points=100,
    )


def test_simple_physical_non_linearity_with_ccd(ccd_5x5: CCD):
    """Test model 'simple_physical_non_linearity' with a 'CCD'."""
    detector = ccd_5x5

    with pytest.raises(TypeError, match="Expecting a 'CMOS' detector object."):
        simple_physical_non_linearity(
            detector=detector,
            cutoff=2.0,
            n_acceptor=1.0e18,
            n_donor=1.0e15,
            diode_diameter=5.0,
            v_bias=0.1,
        )


def test_physical_non_linearity_with_ccd(ccd_5x5: CCD):
    """Test model 'physical_non_linearity' with a 'CCD'."""
    detector = ccd_5x5

    with pytest.raises(TypeError, match="Expecting a 'CMOS' detector object."):
        physical_non_linearity(
            detector=detector,
            cutoff=2.0,
            n_acceptor=1.0e18,
            n_donor=1.0e15,
            diode_diameter=5.0,
            v_bias=0.1,
            fixed_capacitance=5.0e-15,
        )


def test_physical_non_linearity_with_saturation_with_ccd(ccd_5x5: CCD):
    """Test model 'physical_non_linearity_with_saturation' with a 'CCD'."""
    detector = ccd_5x5

    with pytest.raises(TypeError, match="Expecting a 'CMOS' detector object."):
        physical_non_linearity_with_saturation(
            detector=detector,
            cutoff=2.0,
            n_acceptor=1.0e18,
            n_donor=1.0e15,
            phi_implant=5.0,
            d_implant=2.0,
            saturation_current=0.001,
            ideality_factor=1.34,
            v_reset=0.0,
            d_sub=0.220,
            fixed_capacitance=5.0e-15,
            euler_points=100,
        )
