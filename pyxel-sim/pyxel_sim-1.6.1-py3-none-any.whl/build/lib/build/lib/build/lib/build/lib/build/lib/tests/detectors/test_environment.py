#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from copy import deepcopy

import pytest

from pyxel.detectors import Environment


@pytest.mark.parametrize(
    "temperature ",
    [0.0, 1000.0],
)
def test_create_environment(temperature: float):
    """Test when creating a valid `Environment` object."""
    _ = Environment(temperature=temperature)


@pytest.mark.parametrize(
    "temperature, exp_exc, exp_error",
    [
        pytest.param(-0.1, ValueError, r"\'temperature\'"),
        pytest.param(1001, ValueError, r"\'temperature\'"),
    ],
)
def test_create_invalid_environment(temperature: float, exp_exc, exp_error):
    """Test when creating an invalid `Environment` object."""
    with pytest.raises(exp_exc, match=exp_error):
        _ = Environment(temperature=temperature)


@pytest.mark.parametrize(
    "other_obj, is_equal",
    [
        pytest.param(None, False, id="None"),
        pytest.param(Environment(), False, id="Empty 'Environment'"),
        pytest.param(Environment(temperature=100.1), True, id="Valid"),
    ],
)
def test_is_equal(other_obj, is_equal):
    """Test equality statement for Environment."""
    obj = Environment(temperature=100.1)

    if is_equal:
        assert obj == other_obj
    else:
        assert obj != other_obj


@pytest.mark.parametrize(
    "obj, exp_dict",
    [
        (
            Environment(temperature=100.1),
            {"temperature": 100.1},
        )
    ],
)
def test_to_and_from_dict(obj, exp_dict):
    """Test methods 'to_dict' and 'from_dict'"""

    assert type(obj) == Environment

    # Convert from `Environment` to a `dict`
    dct = obj.to_dict()
    assert dct == exp_dict

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    assert copied_dct == exp_dict

    # Convert from `dict` to `Environment`
    other_obj = Environment.from_dict(copied_dct)
    assert type(other_obj) == Environment
    assert obj == other_obj
    assert obj is not other_obj
    assert copied_dct == exp_dict
