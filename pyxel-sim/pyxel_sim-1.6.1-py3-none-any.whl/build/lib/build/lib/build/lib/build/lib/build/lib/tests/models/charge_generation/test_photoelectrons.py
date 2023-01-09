#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#

from pathlib import Path
from typing import Union

import numpy as np
import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.charge_generation import conversion_with_qe_map, simple_conversion


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


@pytest.fixture
def valid_qe_map_path(
    tmp_path: Path,
) -> str:
    """Create valid 2D file on a temporary folder."""
    data_2d = (
        np.array(
            [
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
                [1.0, 1.0, 1.0, 1.0, 1.0],
            ]
        )
        * 0.5
    )

    final_path = f"{tmp_path}/qe.npy"
    np.save(final_path, arr=data_2d)

    return final_path


@pytest.fixture
def invalid_qe_map_path(
    tmp_path: Path,
) -> str:
    """Create valid 2D file on a temporary folder."""

    data_2d = np.array(
        [
            [1.0, 1.0, 0.5, 1.0, 1.0],
            [1.0, 2.0, 1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0, 1.0, 0.0],
            [1.0, 1.0, 1.0, 2.0, 1.0],
            [0.5, 1.0, 1.0, 1.0, 1.0],
        ]
    )

    final_path = f"{tmp_path}/qe.npy"
    np.save(final_path, arr=data_2d)

    return final_path


@pytest.mark.parametrize(
    "qe",
    [
        pytest.param(0.5, id="valid"),
        pytest.param(None, id="valid_none"),
    ],
)
def test_simple_conversion_valid(ccd_5x5: CCD, qe: float):

    detector = ccd_5x5
    detector.characteristics.quantum_efficiency = 0.5

    array = np.ones((5, 5))
    detector.photon.array = array
    target = array * 0.5

    simple_conversion(detector=detector, quantum_efficiency=qe, binomial_sampling=False)

    np.testing.assert_array_almost_equal(detector.charge.array, target)


@pytest.mark.parametrize(
    "qe, exp_exc, exp_error",
    [
        pytest.param(1.5, ValueError, "Quantum efficiency not between 0 and 1."),
    ],
)
def test_simple_conversion_valid2(
    ccd_5x5: CCD,
    qe: float,
    exp_exc,
    exp_error,
):

    with pytest.raises(exp_exc, match=exp_error):
        simple_conversion(detector=ccd_5x5, quantum_efficiency=qe)


def test_conversion_with_qe_valid(ccd_5x5: CCD, valid_qe_map_path: Union[str, Path]):

    detector = ccd_5x5

    conversion_with_qe_map(detector=detector, filename=valid_qe_map_path)


def test_simple_conversion_invalid(ccd_5x5: CCD, invalid_qe_map_path: Union[str, Path]):

    with pytest.raises(
        ValueError, match="Quantum efficiency values not between 0 and 1."
    ):
        conversion_with_qe_map(detector=ccd_5x5, filename=invalid_qe_map_path)
