#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Model for loading PSF from file."""

from pathlib import Path
from typing import Union

import numpy as np
from astropy.convolution import convolve_fft

from pyxel.detectors import Detector
from pyxel.inputs import load_image


def apply_psf(
    array: np.ndarray, psf: np.ndarray, normalize_kernel: bool = True
) -> np.ndarray:
    """Convolve the input array with the point spread function kernel.

    Parameters
    ----------
    array : ndarray
        Input array.
    psf : ndarray
        Convolution kernel.
    normalize_kernel : bool
        Normalize kernel.

    Returns
    -------
    ndarray
    """

    mean = np.mean(array)

    array_2d = convolve_fft(
        array,
        kernel=psf,
        boundary="fill",
        fill_value=mean,
        normalize_kernel=normalize_kernel,
    )

    return array_2d


def load_psf(
    detector: Detector, filename: Union[str, Path], normalize_kernel: bool = True
) -> None:
    """Load a point spread function from file and convolve the photon array with the PSF.

    Parameters
    ----------
    detector : Detector
        Pyxel Detector object.
    filename : Path or str
        Input filename of the point spread function.
    normalize_kernel : bool
        Normalize kernel.
    """
    psf = load_image(filename)

    detector.photon.array = apply_psf(
        array=detector.photon.array, psf=psf, normalize_kernel=normalize_kernel
    )
