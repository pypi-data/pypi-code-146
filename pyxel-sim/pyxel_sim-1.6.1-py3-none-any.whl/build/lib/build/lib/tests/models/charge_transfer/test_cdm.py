#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#

from typing import Optional, Sequence

import numpy as np
import pytest
from typing_extensions import Literal

from pyxel.detectors import (
    CCD,
    CMOS,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
)
from pyxel.models.charge_transfer import cdm


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
        environment=Environment(temperature=273.15),
        characteristics=CCDCharacteristics(),
    )


@pytest.fixture
def input_array() -> np.ndarray:
    """Create a valid input_array."""
    out = np.ones((5, 5), dtype=float) * 1000
    out[:3, :] *= 0
    return out


@pytest.mark.parametrize(
    """
    direction,
    trap_release_times,
    trap_densities,
    sigma,
    beta,
    full_well_capacity,
    max_electron_volume,
    transfer_period,
    charge_injection,
    exp_err,
    exp_exc
    """,
    [
        pytest.param(
            "parallel",
            [1.0],
            [1.0],
            [1.0],
            1.0,
            1.0,
            2.0,
            1.0,
            False,
            ValueError,
            r"'max_electron_volume' must be between 0.0 and 1.0.",
            id="Max volume out of bonds.",
        ),
        pytest.param(
            "parallel",
            [1.0],
            [1.0],
            [1.0],
            2.0,
            1.0,
            1.0,
            1.0,
            False,
            ValueError,
            r"'beta' must be between 0.0 and 1.0.",
            id="Beta out of bonds.",
        ),
        pytest.param(
            "parallel",
            [1.0],
            [1.0],
            [1.0],
            1.0,
            1.0e8,
            1.0,
            1.0,
            False,
            ValueError,
            "'full_well_capacity' must be between 0 and 1e7.",
            id="Fwc out of bonds.",
        ),
        pytest.param(
            "parallel",
            [1.0],
            [1.0],
            [1.0],
            1.0,
            1.0,
            1.0,
            20.0,
            False,
            ValueError,
            r"'transfer_period' must be between 0.0 and 10.0.",
            id="Transfer period out of bonds.",
        ),
        pytest.param(
            "parallel",
            [1.0, 2.0],
            [1.0],
            [1.0],
            1.0,
            1.0,
            1.0,
            1.0,
            False,
            ValueError,
            r"Length of 'sigma', 'trap_densities' and 'trap_release_times' not the same!",
            id="Different lengths.",
        ),
        pytest.param(
            "parallel",
            [],
            [],
            [],
            1.0,
            1.0,
            1.0,
            1.0,
            False,
            ValueError,
            r"Expecting inputs for at least one trap species.",
            id="Empty.",
        ),
    ],
)
def test_cdm_bad_inputs(
    ccd_5x5: CCD,
    direction: Literal["parallel", "serial"],
    beta: float,
    trap_release_times: Sequence[float],
    trap_densities: Sequence[float],
    sigma: Sequence[float],
    full_well_capacity: Optional[float],
    max_electron_volume: float,
    transfer_period: float,
    charge_injection: bool,
    exp_err,
    exp_exc,
):
    """Test function 'cdm' with bad inputs."""
    with pytest.raises(expected_exception=exp_err, match=exp_exc):
        cdm(
            detector=ccd_5x5,
            direction=direction,
            trap_release_times=trap_release_times,
            trap_densities=trap_densities,
            sigma=sigma,
            beta=beta,
            full_well_capacity=full_well_capacity,
            max_electron_volume=max_electron_volume,
            transfer_period=transfer_period,
            charge_injection=charge_injection,
        )


def test_cdm_with_cmos():
    """Test function 'cdm' with CMOS."""

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

    with pytest.raises(
        expected_exception=TypeError, match="Expecting a `CCD` object for 'detector'."
    ):
        cdm(
            detector=detector,
            direction="parallel",
            trap_release_times=[1.0],
            trap_densities=[1.0],
            sigma=[1.0],
            beta=1.0,
            full_well_capacity=1.0,
            max_electron_volume=1.0,
            transfer_period=1.0,
            charge_injection=False,
        )


@pytest.mark.parametrize(
    """
    direction,
    trap_release_times,
    trap_densities,
    sigma,
    beta,
    full_well_capacity,
    max_electron_volume,
    transfer_period,
    charge_injection,
    """,
    [
        pytest.param(
            "parallel",
            [5.0e-3, 5.0e-3],
            [10.0, 10.0],
            [1.0e-15, 1e-15],
            0.3,
            10000.0,
            1.5e-10,
            1.0e-3,
            True,
        ),
    ],
)
def test_cdm_parallel(
    ccd_5x5: CCD,
    input_array: np.ndarray,
    direction: Literal["parallel", "serial"],
    beta: float,
    trap_release_times: Sequence[float],
    trap_densities: Sequence[float],
    sigma: Sequence[float],
    full_well_capacity: Optional[float],
    max_electron_volume: float,
    transfer_period: float,
    charge_injection: bool,
):
    """Test function 'cdm' with valid inputs."""
    expected = np.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [949.71893729, 949.71893729, 949.71893729, 949.71893729, 949.71893729],
            [983.92354165, 983.92354165, 983.92354165, 983.92354165, 983.92354165],
        ]
    )
    detector = ccd_5x5
    detector.pixel.array = input_array

    cdm(
        detector=detector,
        direction=direction,
        trap_release_times=trap_release_times,
        trap_densities=trap_densities,
        sigma=sigma,
        beta=beta,
        full_well_capacity=full_well_capacity,
        max_electron_volume=max_electron_volume,
        transfer_period=transfer_period,
        charge_injection=charge_injection,
    )

    np.testing.assert_array_almost_equal(detector.pixel.array, expected)


@pytest.mark.parametrize(
    """
    direction,
    trap_release_times,
    trap_densities,
    sigma,
    beta,
    full_well_capacity,
    max_electron_volume,
    transfer_period,
    charge_injection,
    """,
    [
        pytest.param(
            "serial",
            [5.0e-3, 5.0e-3],
            [10.0, 10.0],
            [1.0e-15, 1e-15],
            0.3,
            10000.0,
            1.5e-10,
            1.0e-3,
            None,
        ),
    ],
)
def test_cdm_serial(
    ccd_5x5: CCD,
    input_array: np.ndarray,
    direction: Literal["parallel", "serial"],
    beta: float,
    trap_release_times: Sequence[float],
    trap_densities: Sequence[float],
    sigma: Sequence[float],
    full_well_capacity: Optional[float],
    max_electron_volume: float,
    transfer_period: float,
    charge_injection: bool,
):
    """Test function 'cdm' with valid inputs."""
    expected = np.array(
        [
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 0.0, 0.0],
            [1000.0, 989.46583672, 986.54300532, 985.74893059, 985.56511735],
            [1000.0, 989.46583672, 986.54300532, 985.74893059, 985.56511735],
        ]
    )
    detector = ccd_5x5
    detector.pixel.array = input_array

    cdm(
        detector=detector,
        direction=direction,
        trap_release_times=trap_release_times,
        trap_densities=trap_densities,
        sigma=sigma,
        beta=beta,
        full_well_capacity=full_well_capacity,
        max_electron_volume=max_electron_volume,
        transfer_period=transfer_period,
        charge_injection=charge_injection,
    )

    np.testing.assert_array_almost_equal(detector.pixel.array, expected)
