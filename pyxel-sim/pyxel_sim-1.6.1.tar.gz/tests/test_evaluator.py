#   Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#   This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#   is part of this Pyxel package. No part of the package, including
#   this file, may be copied, modified, propagated, or distributed except according to
#   the terms contained in the file ‘LICENCE.txt’.

import pytest

from pyxel.evaluator import eval_range


@pytest.mark.parametrize(
    "expr, exp",
    [
        ("[1,2,3]", [1, 2, 3]),
        ([1, 2, 3], [1, 2, 3]),
        ("numpy.array([1,2,3])", [1, 2, 3]),
        ("numpy.array([1,2,3], dtype=float)", [1.0, 2.0, 3.0]),
        ("numpy.array([1,2,3], dtype=numpy.float64)", [1.0, 2.0, 3.0]),
        ("numpy.array([1,2,3], dtype=int)", [1, 2, 3]),
        ("numpy.array([1,2,3], dtype=numpy.int64)", [1, 2, 3]),
        ("numpy.arange(0, 5, 2)", [0, 2, 4]),
        ("_", ["_"]),
    ],
)
def test_eval_range(expr: str, exp):
    """Test function 'eval_range'."""
    value = eval_range(expr)
    assert value == exp


@pytest.mark.parametrize(
    "expr, exp_exc, exp_msg",
    [
        (
            "numpy.array([1,2,3], dtype=numpy.float32)",
            NotImplementedError,
            "numpy data type is not a float or int",
        ),
        (
            "numpy.array([1,2,3], dtype=numpy.uint64)",
            NotImplementedError,
            "numpy data type is not a float or int",
        ),
        ("np.array([1,2,3])", NameError, r"name \'np\' is not defined"),
        (1, NotImplementedError, ""),
    ],
)
def test_eval_range_failing(expr: str, exp_exc: Exception, exp_msg: str):
    """Test function 'eval_range' with bad inputs."""
    with pytest.raises(exp_exc, match=exp_msg):
        _ = eval_range(expr)
