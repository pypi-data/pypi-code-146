#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import numpy as np
import pytest

from pyxel.models.readout_electronics.amplifier_crosstalk import get_channel_slices


@pytest.fixture()
def shape():
    return 100, 100


@pytest.mark.parametrize(
    "channel_matrix,expected",
    [
        (np.array([1, 2]), [[(0, 50), (0, 100)], [(50, 100), (0, 100)]]),
        (
            np.array([[4, 3], [1, 2]]),
            [
                [(0, 50), (50, 100)],
                [(50, 100), (50, 100)],
                [(50, 100), (0, 50)],
                [(0, 50), (0, 50)],
            ],
        ),
    ],
)
def test_channel_slices(shape, channel_matrix, expected):
    assert get_channel_slices(shape, channel_matrix) == expected
