#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import pytest

from pyxel.calibration.util import slice_to_range


@pytest.mark.parametrize(
    "data, exp_result",
    [
        pytest.param(slice(10), range(10), id="0 to 10"),
        pytest.param(slice(20, 30), range(20, 30), id="20 to 30"),
    ],
)
def test_slice_to_range(data, exp_result):
    """Test function 'slice_to_range' with valid inputs."""
    result = slice_to_range(data)
    assert result == exp_result


@pytest.mark.parametrize(
    "data, exp_exp, exp_msg",
    [
        pytest.param(
            slice(10, 20, 2),
            ValueError,
            "Cannot use parameter 'step' in the slice object",
            id="with_step",
        ),
        pytest.param(
            slice(5, None),
            ValueError,
            "Missing 'stop' parameter in the slice object",
            id="No 'stop'",
        ),
        pytest.param(
            slice(0),
            ValueError,
            "Parameter 'stop' must be strictly greater than 'start'",
            id="'stop' == 0",
        ),
        pytest.param(
            slice(5, 5),
            ValueError,
            "Parameter 'stop' must be strictly greater than 'start'",
            id="'stop' == 'start'",
        ),
        pytest.param(
            slice(5, 4),
            ValueError,
            "Parameter 'stop' must be strictly greater than 'start'",
            id="'stop' smaller than 'start'",
        ),
        pytest.param(
            slice(-1, 4),
            ValueError,
            "Parameter 'start' must be strictly positive",
            id="negative 'start'",
        ),
    ],
)
def test_slice_to_range_bad_inputs(data, exp_exp, exp_msg):
    """Test function 'slice_to_range' with invalid inputs."""
    with pytest.raises(exp_exp, match=exp_msg):
        _ = slice_to_range(data)
