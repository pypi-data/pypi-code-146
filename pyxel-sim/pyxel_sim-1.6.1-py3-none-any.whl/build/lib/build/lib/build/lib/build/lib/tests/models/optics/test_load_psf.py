#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Tests for load psf model."""
from pathlib import Path

import numpy as np
import pytest

from pyxel.detectors import (
    CCD,
    CCDCharacteristics,
    CCDGeometry,
    Detector,
    Environment,
    ReadoutProperties,
)
from pyxel.models.optics import load_psf


@pytest.fixture
def ccd_10x10() -> CCD:
    """Create a valid CCD detector."""
    detector = CCD(
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
    detector._readout_properties = ReadoutProperties(num_steps=1)
    return detector


@pytest.fixture
def psf_10x10() -> np.ndarray:
    """Create a gaussian psf of 10x10."""
    shape = (10, 10)
    ny, nx = (el / 2 for el in shape)
    ay, ax = (np.arange(-el / 2.0 + 0.5, el / 2.0 + 0.5) for el in shape)
    xx, yy = np.meshgrid(ax, ay, indexing="xy")
    r = ((xx / nx) ** 2 + (yy / ny) ** 2) ** 0.5
    out = np.ones(shape)
    sigma = 0.5
    out[...] = np.exp(-(r**2) / (2 * sigma**2)) / (np.sqrt(2 * np.pi) * sigma)
    return out


@pytest.fixture
def psf_10x10_npy_filename(psf_10x10: np.ndarray, tmp_path: Path) -> Path:
    """Create a filename with a psf 10x10."""
    filename = tmp_path / "psf.npy"
    np.save(filename, psf_10x10)
    return filename


def test_load_psf(ccd_10x10: CCD, psf_10x10_npy_filename: Path) -> None:
    """Test function 'load_psf'."""
    detector: Detector = ccd_10x10

    # Run model
    load_psf(
        detector=detector,
        filename=psf_10x10_npy_filename,
    )
