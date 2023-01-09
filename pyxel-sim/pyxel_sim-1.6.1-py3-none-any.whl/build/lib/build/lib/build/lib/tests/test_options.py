#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from pathlib import Path
from typing import Optional, Type

import pytest

import pyxel
from pyxel.options import GlobalOptions, global_options


def test_with_context_manager():
    """Test with embedded context managers."""
    assert global_options == GlobalOptions()

    with pyxel.set_options(cache_folder="dummy"):
        assert global_options == GlobalOptions(cache_folder="dummy")

        with pyxel.set_options(cache_folder=Path("foo"), cache_enabled=True):
            assert global_options == GlobalOptions(
                cache_folder=Path("foo"), cache_enabled=True
            )

        assert global_options == GlobalOptions(cache_folder="dummy")

    assert global_options == GlobalOptions()


def test_global():
    assert global_options == GlobalOptions()

    pyxel.set_options(cache_folder="dummy")
    assert global_options == GlobalOptions(cache_folder="dummy")

    pyxel.set_options(cache_folder=None)
    assert global_options == GlobalOptions()


@pytest.mark.parametrize(
    "dct, exp_error, exp_msg",
    [
        pytest.param(
            {"non_sense": "foo"}, KeyError, "Wrong option", id="Unknown option"
        ),
        pytest.param({"cache_enabled": "Hello"}, TypeError, None, id="Wrong type"),
        pytest.param({"cache_folder": 42}, TypeError, None, id="Wrong type"),
    ],
)
def test_with_wrong_inputs(
    dct: dict, exp_error: Type[TypeError], exp_msg: Optional[str]
):
    """Test with a bad input."""
    with pytest.raises(exp_error, match=exp_msg):
        pyxel.set_options(**dct)
