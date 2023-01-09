#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

"""TBW."""

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from pyxel.detectors import CCD

try:
    import arcticpy as ac

    WITH_ARTICPY = True
except ImportError:
    # No 'arcticpy' library
    WITH_ARTICPY = False


@dataclass
class Trap:
    """Define a trap.

    Parameters
    ----------
    density : float
        The density of the trap species in a pixel.
    release_timescale : float
        The release timescale of the trap.
    """

    density: float
    release_timescale: float


def compute_arctic_add(
    image_2d: np.ndarray,
    full_well_depth: float,
    well_fill_power: float,
    parallel_traps: Sequence[Trap],
    parallel_express: int,
) -> np.ndarray:
    """Create a new image with :term:`CTI` trails.

    Parameters
    ----------
    image_2d : ndarray
        2D image to process.
    full_well_depth : float
    well_fill_power : float
    parallel_traps : sequence of Traps
        List of trap to process.
    parallel_express : int

    Returns
    -------
    ndarray
        2D array with :term:`CTI` trails.
    """
    ccd = ac.CCD(
        phases=[
            ac.CCDPhase(
                full_well_depth=full_well_depth,
                well_fill_power=well_fill_power,
            )
        ]
    )

    roe = ac.ROE()

    # Create the trap(s)
    traps: Sequence[ac.TrapInstantCapture] = [
        ac.TrapInstantCapture(
            density=trap.density,
            release_timescale=trap.release_timescale,
        )
        for trap in parallel_traps
    ]

    image_cti_added_2d = ac.add_cti(
        image=image_2d,
        parallel_traps=traps,
        parallel_ccd=ccd,
        parallel_roe=roe,
        parallel_express=parallel_express,
        verbosity=0,
    )

    return image_cti_added_2d


def arctic_add(
    detector: CCD,
    well_fill_power: float,
    trap_densities: Sequence[float],
    trap_release_timescales: Sequence[float],
    express: int = 0,
) -> None:
    """Add :term:`CTI` trails to an image by trapping, releasing and moving electrons.

    Parameters
    ----------
    detector : CCD
        Pyxel :term:`CCD` Detector object.
    well_fill_power : float
    trap_densities : sequence of float
        A 1D arrays of all trap species densities for serial clocking.
    trap_release_timescales : sequence of float
        A 1D arrays of all trap release timescales for serial clocking.
    express : int
        As described in more detail in :cite:p:`2014:massey` section 2.1.5, the effects
        of each individual pixel-to-pixel transfer can be very similar, so multiple
        transfers can be computed at once for efficiency.
        The ``express`` input sets the number of times the transfers are calculated.

            * ``express = 1`` is the fastest and least accurate.
            * ``express = 2`` means the transfers are re-computed half-way through readout.
            * ``express = N`` where ``N`` is the total number of pixels.

        Default ``express = 0`` is a convenient input for automatic ``express = N``.

    Notes
    -----
    The external library `arcticpy <https://github.com/jkeger/arcticpy>`_ is used to add
    the :term:`CTI` trails.
    """
    # Validation
    if len(trap_densities) != len(trap_release_timescales):
        raise ValueError(
            "Expecting same number of 'trap_densities' and 'trap_release_timescales'"
        )

    if len(trap_densities) == 0:
        raise ValueError("Expecting at least one 'trap_density'.")

    # Conversion - Create a list of `Trap`
    traps: Sequence[Trap] = [
        Trap(density=density, release_timescale=release_timescale)
        for density, release_timescale in zip(trap_densities, trap_release_timescales)
    ]

    if not WITH_ARTICPY:
        raise RuntimeError(
            "ArCTIC python wrapper is not installed ! "
            "See https://github.com/jkeger/arctic"
        )

    image_cti_added_2d = compute_arctic_add(
        image_2d=np.asarray(detector.pixel.array, dtype=float),
        full_well_depth=detector.characteristics.full_well_capacity,
        well_fill_power=well_fill_power,
        parallel_traps=traps,
        parallel_express=express,
    )

    detector.pixel.array = image_cti_added_2d


def compute_arctic_remove(
    image_2d: np.ndarray,
    full_well_depth: float,
    well_fill_power: float,
    parallel_traps: Sequence[Trap],
    parallel_express: int,
    num_iterations: int,
) -> np.ndarray:
    """Create a new image with removed :term:`CTI` trails.

    Parameters
    ----------
    image_2d : ndarray
        2D image to process.
    full_well_depth : float
    well_fill_power : float
    parallel_traps : sequence of Traps
        List of trap to process.
    parallel_express : int
    num_iterations : int

    Returns
    -------
    ndarray
        2D array without :term:`CTI` trails.
    """
    ccd = ac.CCD(well_fill_power=well_fill_power, full_well_depth=full_well_depth)
    roe = ac.ROE()

    # Build the traps
    traps: Sequence[ac.TrapInstantCapture] = [
        ac.TrapInstantCapture(
            density=trap.density,
            release_timescale=trap.release_timescale,
        )
        for trap in parallel_traps
    ]

    # Remove CTI
    image_2d_cti_removed = ac.remove_cti(
        image=image_2d,
        n_iterations=num_iterations,
        parallel_traps=traps,
        parallel_ccd=ccd,
        parallel_roe=roe,
        parallel_express=parallel_express,
    )

    return image_2d_cti_removed


def arctic_remove(
    detector: CCD,
    well_fill_power: float,
    trap_densities: Sequence[float],
    trap_release_timescales: Sequence[float],
    num_iterations: int,
    express: int = 0,
) -> None:
    """Remove :term:`CTI` trails from an image by first modelling the addition of :term:`CTI`.

    Parameters
    ----------
    detector : CCD
        Pyxel :term:`CCD` Detector object.
    well_fill_power : float
    trap_densities
    trap_release_timescales
    num_iterations : int
        Number of iterations for the forward modelling.
        More iterations provide higher accuracy at the cost of longer runtime.
        In practice, just 1 to 3 iterations are usually sufficient.
    express : int
        As described in more detail in :cite:p:`2014:massey` section 2.1.5, the effects
        of each individual pixel-to-pixel transfer can be very similar, so multiple
        transfers can be computed at once for efficiency.
        The ``express`` input sets the number of times the transfers are calculated.

            * ``express = 1`` is the fastest and least accurate.
            * ``express = 2`` means the transfers are re-computed half-way through readout.
            * ``express = N`` where ``N`` is the total number of pixels.

        Default ``express = 0`` is a convenient input for automatic ``express = N``.
    """
    # Validation
    if len(trap_densities) != len(trap_release_timescales):
        raise ValueError(
            "Expecting same number of 'trap_densities' and 'trap_release_timescales'"
        )
    if len(trap_densities) == 0:
        raise ValueError("Expecting at least one 'trap_density'.")
    if num_iterations <= 0:
        raise ValueError("Number of iterations must be > 1.")

    # Conversion
    traps: Sequence[Trap] = [
        Trap(density=density, release_timescale=release_timescale)
        for density, release_timescale in zip(trap_densities, trap_release_timescales)
    ]

    if not WITH_ARTICPY:
        raise RuntimeError(
            "ArCTIC python wrapper is not installed ! "
            "See https://github.com/jkeger/arctic"
        )

    image_2d_cti_removed = compute_arctic_remove(
        image_2d=np.asarray(detector.pixel.array, dtype=float),
        full_well_depth=detector.characteristics.full_well_capacity,
        well_fill_power=well_fill_power,
        parallel_traps=traps,
        parallel_express=express,
        num_iterations=num_iterations,
    )

    detector.pixel.array = image_2d_cti_removed
