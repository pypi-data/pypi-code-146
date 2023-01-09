#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.charge_transfer import arctic_add


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
    "trap_densities, trap_release_timescales, exp_exc",
    [
        pytest.param([], [], "Expecting at least one 'trap_density'", id="no trap"),
        pytest.param(
            [1],
            [1, 2],
            "Expecting same number of 'trap_densities' and 'trap_release_timescales'",
            id="no trap",
        ),
    ],
)
def test_arctic_add_bad_inputs(
    ccd_10x10: CCD, trap_densities, trap_release_timescales, exp_exc
):
    """Test function 'arctic_add' with bad inputs."""
    with pytest.raises(ValueError, match=exp_exc):
        arctic_add(
            detector=ccd_10x10,
            well_fill_power=1.0,
            trap_densities=trap_densities,
            trap_release_timescales=trap_release_timescales,
            express=0,
        )
