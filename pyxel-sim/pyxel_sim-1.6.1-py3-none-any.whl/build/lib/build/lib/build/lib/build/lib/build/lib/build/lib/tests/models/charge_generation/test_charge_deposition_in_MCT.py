#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.


from pathlib import Path

import pytest

from pyxel.models.charge_generation.charge_deposition import simulate_charge_deposition


def test_simulate_charge_deposition_number_of_particles() -> None:

    flux = 0
    exposure = 1
    x_lim = 50
    y_lim = 50
    z_lim = 50
    step_size = 1
    energy_mean = 1
    energy_spread = 1
    energy_spectrum = None
    energy_spectrum_sampling = "log"
    ehpair_creation = 3.65
    material_density = 2.3290
    particle_direction = None
    stopping_power_curve = "data/mct-stopping-power.csv"

    # Run model
    with pytest.raises(
        ValueError, match="The number of particles generated has to be greater than 0."
    ):
        simulate_charge_deposition(
            flux=flux,
            exposure=exposure,
            x_lim=x_lim,
            y_lim=y_lim,
            z_lim=z_lim,
            step_size=step_size,
            energy_mean=energy_mean,
            energy_spread=energy_spread,
            energy_spectrum=energy_spectrum,
            energy_spectrum_sampling=energy_spectrum_sampling,
            ehpair_creation=ehpair_creation,
            material_density=material_density,
            particle_direction=particle_direction,
            stopping_power_curve=stopping_power_curve,
        )


@pytest.mark.parametrize("x_lim,y_lim,z_lim", [(-1, 2, 4), (2, -1, 4), (2, 1, -4)])
def test_simulate_charge_deposition_sampling_argument(x_lim, y_lim, z_lim) -> None:

    flux = 1
    exposure = 1
    step_size = 1
    energy_mean = 1
    energy_spread = 1
    energy_spectrum = None
    energy_spectrum_sampling = 1
    ehpair_creation = 3.65
    material_density = 2.3290
    particle_direction = None
    stopping_power_curve = Path(
        "pyxel/models/charge_generation/data/mct-stopping-power.csv"
    ).resolve()

    # Run model
    with pytest.raises(ValueError, match="Detector dimension is negative or 0."):
        simulate_charge_deposition(
            flux=flux,
            exposure=exposure,
            x_lim=x_lim,
            y_lim=y_lim,
            z_lim=z_lim,
            step_size=step_size,
            energy_mean=energy_mean,
            energy_spread=energy_spread,
            energy_spectrum=energy_spectrum,
            energy_spectrum_sampling=energy_spectrum_sampling,
            ehpair_creation=ehpair_creation,
            material_density=material_density,
            particle_direction=particle_direction,
            stopping_power_curve=str(stopping_power_curve),
        )
