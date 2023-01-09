#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
import numpy as np
import pytest

from pyxel.detectors import CCD, CCDCharacteristics, CCDGeometry, Environment
from pyxel.models.photon_generation import shot_noise


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


def test_shot_noise_poisson(ccd_10x10: CCD):
    """Test for model shot_noise."""

    detector = ccd_10x10

    detector.photon.array = np.ones(detector.photon.shape) * 10

    shot_noise(
        detector=detector,
        type="poisson",
        seed=0,
    )

    data_2d = np.array(
        [
            [10.0, 11.0, 9.0, 9.0, 18.0, 13.0, 4.0, 10.0, 10.0, 8.0],
            [10.0, 11.0, 16.0, 9.0, 12.0, 12.0, 7.0, 8.0, 11.0, 7.0],
            [11.0, 10.0, 6.0, 11.0, 7.0, 13.0, 14.0, 12.0, 8.0, 8.0],
            [8.0, 11.0, 10.0, 8.0, 6.0, 8.0, 11.0, 13.0, 12.0, 7.0],
            [11.0, 9.0, 12.0, 13.0, 14.0, 14.0, 12.0, 17.0, 9.0, 12.0],
            [11.0, 6.0, 11.0, 11.0, 11.0, 15.0, 9.0, 13.0, 6.0, 6.0],
            [13.0, 9.0, 12.0, 12.0, 10.0, 7.0, 13.0, 12.0, 6.0, 11.0],
            [16.0, 10.0, 12.0, 9.0, 12.0, 7.0, 4.0, 8.0, 9.0, 12.0],
            [10.0, 12.0, 8.0, 11.0, 8.0, 12.0, 7.0, 10.0, 7.0, 9.0],
            [8.0, 14.0, 10.0, 12.0, 11.0, 6.0, 9.0, 15.0, 10.0, 18.0],
        ]
    )

    photon = detector.photon.array

    assert data_2d.dtype == photon.dtype
    np.testing.assert_array_almost_equal(photon, data_2d)


def test_shot_noise_normal(ccd_10x10: CCD):
    """Test for model shot_noise."""

    detector = ccd_10x10

    detector.photon.array = np.ones(detector.photon.shape) * 10

    shot_noise(
        detector=detector,
        type="normal",
        seed=0,
    )

    data_2d = np.array(
        [
            [
                15.57842333,
                11.2654082,
                13.09504126,
                17.0863265,
                15.90573691,
                6.90957599,
                13.00444338,
                9.52136648,
                9.67359333,
                11.29842647,
            ],
            [
                10.45550577,
                14.59881662,
                12.4066126,
                10.38477019,
                11.40361879,
                11.05517087,
                14.72469288,
                9.35123261,
                10.990007,
                7.29911212,
            ],
            [
                1.92673734,
                12.06692348,
                12.73358728,
                7.65306814,
                17.17759434,
                5.40089192,
                10.14470114,
                9.40807269,
                14.84707347,
                14.64652041,
            ],
            [
                10.48998678,
                11.19585489,
                7.19257496,
                3.73617158,
                8.89980518,
                10.49441885,
                13.89052074,
                13.80225893,
                8.77516506,
                9.04403477,
            ],
            [
                6.68418438,
                5.509509,
                4.60429989,
                16.16889345,
                8.38833829,
                8.61468742,
                6.03831322,
                12.45864038,
                4.89640689,
                9.32725616,
            ],
            [
                7.1682861,
                11.22349313,
                8.38469232,
                6.26651322,
                9.91087997,
                11.35450431,
                10.21034593,
                10.95650013,
                7.99409741,
                8.85291171,
            ],
            [
                7.87349335,
                8.86299307,
                7.42860568,
                4.54101509,
                10.56107073,
                8.72945712,
                4.84486019,
                11.46344599,
                7.13087065,
                10.16426576,
            ],
            [
                12.3055868,
                10.40787978,
                13.60310133,
                6.09513789,
                11.27231598,
                7.83444035,
                7.24629763,
                8.16951664,
                9.01478439,
                10.17761041,
            ],
            [
                6.31547269,
                12.84866348,
                11.47255393,
                5.14197091,
                14.70626667,
                15.99532799,
                13.7276283,
                9.43102771,
                6.61398291,
                13.33446914,
            ],
            [
                8.72504255,
                13.86571074,
                10.65862331,
                13.08840381,
                11.1269295,
                12.23438055,
                10.03320398,
                15.64741837,
                10.40133128,
                11.27120198,
            ],
        ]
    )

    photon = detector.photon.array

    assert data_2d.dtype == photon.dtype
    np.testing.assert_array_almost_equal(photon, data_2d)
