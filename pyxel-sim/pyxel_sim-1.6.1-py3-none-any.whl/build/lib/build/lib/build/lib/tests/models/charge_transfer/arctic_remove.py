#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.charge_transfer import arctic_remove


@pytest.fixture
def ccd_10x10() -> CCD:
    """Create a valid CCD detector."""
    return CCD(
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


@pytest.mark.parametrize(
    "num_iterations, instant_traps, exp_exc, exp_msg",
    [
        pytest.param(
            0,
            [{"density": 1.0, "release_timescale": 10.0}],
            ValueError,
            "Number of iterations must be > 1",
            id="num_iterations == 0",
        ),
        pytest.param(
            -1,
            [{"density": 1.0, "release_timescale": 10.0}],
            ValueError,
            "Number of iterations must be > 1",
            id="num_iterations < 0",
        ),
        pytest.param(
            1,
            [{"release_timescale": 10.0}],
            KeyError,
            "Missing key 'density' in parameter 'instant_traps'",
            id="num_iterations < 0",
        ),
        pytest.param(
            1,
            [{"density": 1.0}],
            KeyError,
            "Missing key 'release_timescale' in parameter 'instant_traps'",
            id="num_iterations < 0",
        ),
    ],
)
def test_arctic_remove_bad_inputs(
    ccd_10x10: CCD, num_iterations, instant_traps, exp_exc, exp_msg
):
    """Test function 'arctic_remove' with bad inputs."""
    with pytest.raises(exp_exc, match=exp_msg):
        arctic_remove(
            detector=ccd_10x10,
            well_fill_power=10.0,
            instant_traps=instant_traps,
            num_iterations=num_iterations,
            express=0,
        )
