#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

import pytest
import xarray as xr

from pyxel.data_structure import ProcessedData


@pytest.mark.parametrize(
    "input_data, exp_data",
    [
        (None, xr.Dataset()),
        (
            xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])}),
            xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])}),
        ),
        (
            xr.DataArray([1, 2, 3], dims=["x"], name="foo"),
            xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])}),
        ),
    ],
)
def test_init(input_data, exp_data):
    """Test method 'ProcessedData.__init__'."""
    obj = ProcessedData(input_data)

    assert isinstance(obj.data, xr.Dataset)
    xr.testing.assert_equal(obj.data, exp_data)


def test_init_wrong():
    """Test method 'ProcessedData.__init__' with bad input."""
    with pytest.raises(ValueError, match="Missing parameter 'name' in the 'DataArray'"):
        _ = ProcessedData(xr.DataArray([1, 2, 3], dims=["x"]))


@pytest.mark.parametrize(
    "obj, other, exp",
    [
        (ProcessedData(), ProcessedData(), True),
        (
            ProcessedData(xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])})),
            ProcessedData(xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])})),
            True,
        ),
        (
            ProcessedData(xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])})),
            ProcessedData(xr.Dataset({"bar": xr.DataArray([1, 2, 3], dims=["x"])})),
            False,
        ),
        (
            ProcessedData(xr.Dataset({"foo": xr.DataArray([1, 2, 3], dims=["x"])})),
            ProcessedData(xr.DataArray([1, 2, 3], dims=["x"], name="foo")),
            True,
        ),
    ],
)
def test_eq(obj, other, exp):
    """Test method 'ProcessedData.__eq__'."""
    if exp:
        assert obj == other
    else:
        assert obj != other


def test_append():
    """Test method 'ProcessedData.append'."""
    obj = ProcessedData()

    # First '.append'
    obj.append(
        xr.Dataset(
            data_vars={"foo": xr.DataArray([10, 20], dims=["x"], coords={"x": [1, 2]})}
        )
    )
    xr.testing.assert_equal(
        obj.data,
        xr.Dataset(
            data_vars={"foo": xr.DataArray([10, 20], dims=["x"])},
            coords={"x": [1, 2]},
        ),
    )

    # Second '.append'
    obj.append(
        xr.Dataset(
            data_vars={"foo": xr.DataArray([30, 40], dims=["x"], coords={"x": [3, 4]})}
        )
    )
    xr.testing.assert_equal(
        obj.data,
        xr.Dataset(
            data_vars={"foo": xr.DataArray([10, 20, 30, 40], dims=["x"])},
            coords={"x": [1, 2, 3, 4]},
        ),
    )


def test_append_multi_dimension():
    """Test method 'ProcessedData.append' with multidimensional data."""
    obj = ProcessedData()

    # First '.append'
    obj.append(
        xr.DataArray(
            [[10, 20]], dims=["y", "x"], coords={"x": [1, 2], "y": [1]}, name="foo"
        )
    )
    xr.testing.assert_equal(
        obj.data,
        xr.Dataset(
            data_vars={"foo": xr.DataArray([[10, 20]], dims=["y", "x"])},
            coords={"x": [1, 2], "y": [1]},
        ),
    )

    # Second '.append'
    obj.append(
        xr.DataArray([[30, 40]], dims=["y", "x"], coords={"x": [1, 2], "y": [2]}),
        default_name="foo",
    )
    xr.testing.assert_equal(
        obj.data,
        xr.Dataset(
            data_vars={"foo": xr.DataArray([[10, 20], [30, 40]], dims=["y", "x"])},
            coords={"x": [1, 2], "y": [1, 2]},
        ),
    )
