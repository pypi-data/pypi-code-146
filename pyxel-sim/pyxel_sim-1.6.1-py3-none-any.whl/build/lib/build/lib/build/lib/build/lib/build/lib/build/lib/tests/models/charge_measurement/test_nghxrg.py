#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import numpy as np
import pytest

from pyxel.detectors import CMOS, CMOSCharacteristics, CMOSGeometry, Environment
from pyxel.models.charge_measurement import nghxrg


@pytest.fixture
def cmos_10x10() -> CMOS:
    """Create a valid CCD detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=10,
            col=10,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CMOSCharacteristics(),
    )

    # Generate fake pixels
    rs = np.random.RandomState(12345)
    detector.pixel.array = rs.normal(loc=10000, scale=500, size=(10, 10))

    return detector


@pytest.fixture
def cmos_10x15() -> CMOS:
    """Create a valid CCD detector."""
    detector = CMOS(
        geometry=CMOSGeometry(
            row=10,
            col=15,
            total_thickness=40.0,
            pixel_vert_size=10.0,
            pixel_horz_size=10.0,
        ),
        environment=Environment(),
        characteristics=CMOSCharacteristics(),
    )

    # Generate fake pixels
    rs = np.random.RandomState(12345)
    detector.pixel.array = rs.normal(loc=10000, scale=500, size=(10, 15))

    return detector


def test_nghxrg_10x10(cmos_10x10: CMOS):
    """Test model 'nghxrg' without parameters."""

    noise = [
        {"ktc_bias_noise": {"ktc_noise": 1, "bias_offset": 2, "bias_amp": 2}},
        {"white_read_noise": {"rd_noise": 1, "ref_pixel_noise_ratio": 2}},
        {"corr_pink_noise": {"c_pink": 1.0}},
        {"uncorr_pink_noise": {"u_pink": 1.0}},
        {"acn_noise": {"acn": 1.0}},
        {"pca_zero_noise": {"pca0_amp": 1.0}},
    ]

    nghxrg(detector=cmos_10x10, noise=noise)


# TODO: This test fails because 'y' and 'x' are not in the right order
def test_nghxrg_10x15(cmos_10x15: CMOS):
    """Test model 'nghxrg' without parameters."""

    noise = [
        {"ktc_bias_noise": {"ktc_noise": 1, "bias_offset": 2, "bias_amp": 2}},
        {"white_read_noise": {"rd_noise": 1, "ref_pixel_noise_ratio": 2}},
        {"corr_pink_noise": {"c_pink": 1.0}},
        {"uncorr_pink_noise": {"u_pink": 1.0}},
        {"acn_noise": {"acn": 1.0}},
        {"pca_zero_noise": {"pca0_amp": 1.0}},
    ]

    nghxrg(detector=cmos_10x15, noise=noise)
