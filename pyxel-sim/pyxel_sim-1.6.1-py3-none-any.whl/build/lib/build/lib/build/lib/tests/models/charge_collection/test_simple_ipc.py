#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.
#
#
"""Tests for simple inter-pixel capacitance model."""

import numpy as np
import pytest

from pyxel.detectors import (
    CCD,
    CMOS,
    CCDCharacteristics,
    CCDGeometry,
    CMOSCharacteristics,
    CMOSGeometry,
    Environment,
)
from pyxel.models.charge_collection import simple_ipc


@pytest.fixture
def cmos_10x10() -> CMOS:
    """Create a valid CCD detector."""
    return CMOS(
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


def test_simple_ipc_valid(cmos_10x10: CMOS):
    """Test model 'simple_ipc' with valid inputs."""
    detector = cmos_10x10
    detector.pixel.array = np.array(
        [
            [
                35.92755861,
                39.866901,
                40.21125602,
                16.53336642,
                98.25807141,
                14.77660117,
                10.38839134,
                82.91567845,
                61.20595539,
                44.99545736,
            ],
            [
                51.56561303,
                56.22059037,
                31.52724539,
                72.13462645,
                84.85798493,
                99.95004718,
                54.87959409,
                15.4897156,
                10.71639319,
                54.65712507,
            ],
            [
                14.999205,
                32.09393403,
                5.16630696,
                47.00578722,
                93.45200407,
                95.78382619,
                49.24008654,
                30.45493009,
                65.98544986,
                81.02105842,
            ],
            [
                71.02466145,
                37.10067213,
                0.27268097,
                65.55902007,
                2.61932674,
                14.03845251,
                5.25876994,
                29.25754102,
                96.75829445,
                41.47556914,
            ],
            [
                6.74229451,
                89.02694184,
                51.2699751,
                17.20487056,
                57.87485843,
                73.86680132,
                5.78593678,
                44.39522596,
                53.49792232,
                97.03850645,
            ],
            [
                24.04553442,
                26.41334873,
                90.13179938,
                37.42229458,
                87.6545525,
                26.88294484,
                53.61090853,
                62.78018977,
                48.5720461,
                53.04157629,
            ],
            [
                17.87004508,
                96.90631019,
                67.72783903,
                83.85671912,
                26.63495226,
                32.66135426,
                72.73868042,
                31.00822857,
                87.21205869,
                93.55887689,
            ],
            [
                39.93814078,
                22.21643716,
                49.84485408,
                84.53971696,
                19.92218508,
                68.91319857,
                47.31780822,
                91.1972756,
                98.55693513,
                27.30498608,
            ],
            [
                24.36348034,
                22.70919245,
                92.10489024,
                98.30190277,
                56.12779963,
                86.56174902,
                28.65707854,
                54.91590922,
                3.9133337,
                99.25525741,
            ],
            [
                69.7156563,
                6.14548824,
                83.95726626,
                79.88813728,
                54.68671223,
                78.86641073,
                63.71629964,
                36.73631978,
                54.65512014,
                56.7133959,
            ],
        ]
    )

    expected_array = np.array(
        [
            [
                44.08622098,
                42.73208842,
                40.83840307,
                44.28024238,
                66.71501485,
                42.81526075,
                35.26611049,
                55.63481379,
                54.16551724,
                48.42865354,
            ],
            [
                46.99992841,
                43.14278252,
                39.24850518,
                60.2860532,
                78.43888588,
                78.45206173,
                52.32955204,
                32.00030134,
                34.27840115,
                50.33879875,
            ],
            [
                35.32136701,
                29.71108858,
                26.12622684,
                47.22511248,
                74.6509705,
                72.22348102,
                48.25354623,
                38.67425231,
                55.45328413,
                64.99164607,
            ],
            [
                52.71299196,
                36.49627376,
                26.6719488,
                41.4824723,
                33.68134677,
                28.83272179,
                23.80884795,
                38.93021548,
                68.9079442,
                59.50923533,
            ],
            [
                36.00312624,
                56.87208706,
                48.97120605,
                37.31338659,
                48.50356786,
                48.14429961,
                28.45727216,
                42.11763417,
                59.28642179,
                71.55494093,
            ],
            [
                35.97356672,
                45.60422821,
                67.03094246,
                55.3308361,
                59.71667614,
                44.72638016,
                47.69387462,
                54.63583174,
                57.63538859,
                59.81040364,
            ],
            [
                38.55827616,
                63.49235046,
                68.91828504,
                66.72486088,
                44.21960982,
                43.11411671,
                56.92620855,
                56.37819499,
                73.09377726,
                73.64391806,
            ],
            [
                39.7026063,
                39.03476212,
                60.09323894,
                67.76647947,
                48.78023194,
                53.86002133,
                57.09655011,
                71.08337409,
                75.14375914,
                53.68974626,
            ],
            [
                33.69354046,
                38.3826958,
                71.57903588,
                80.52151147,
                67.31639057,
                65.27345668,
                51.41297477,
                48.36817711,
                42.93002788,
                65.65481709,
            ],
            [
                49.63795722,
                38.6459351,
                66.06237277,
                73.06893768,
                64.48210257,
                66.03472005,
                58.39195111,
                44.35264462,
                50.79020066,
                55.04593666,
            ],
        ]
    )

    simple_ipc(
        detector=cmos_10x10,
        coupling=0.1,
        diagonal_coupling=0.05,
        anisotropic_coupling=0.03,
    )
    print(detector.pixel.array)
    np.testing.assert_array_almost_equal(detector.pixel.array, expected_array)


@pytest.mark.parametrize(
    "coupling, diagonal_coupling, anisotropic_coupling, exp_exc, exp_error",
    [
        pytest.param(
            0.05,
            0.08,
            0.01,
            ValueError,
            "Requirement diagonal_coupling <= coupling is not met.",
        ),
        pytest.param(
            0.03,
            0.02,
            0.05,
            ValueError,
            "Requirement anisotropic_coupling <= coupling is not met.",
        ),
        pytest.param(
            0.2,
            0.1,
            0.01,
            ValueError,
            r"Requirement coupling \+ diagonal_coupling << 1 is not met.",
        ),
    ],
)
def test_charge_blocks_inputs(
    cmos_10x10: CMOS,
    coupling: float,
    diagonal_coupling: float,
    anisotropic_coupling: float,
    exp_exc,
    exp_error,
):
    """Test model 'charge_blocks' with bad inputs."""
    with pytest.raises(exp_exc, match=exp_error):
        simple_ipc(
            detector=cmos_10x10,
            coupling=coupling,
            diagonal_coupling=diagonal_coupling,
            anisotropic_coupling=anisotropic_coupling,
        )


def test_charge_blocks_with_ccd():
    """Test model 'charge_blocks' with a `CCD` detector."""
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

    with pytest.raises(TypeError, match="Expecting a CMOS object for detector."):
        simple_ipc(
            detector=detector,
            coupling=0.1,
            diagonal_coupling=0.05,
            anisotropic_coupling=0.03,
        )
