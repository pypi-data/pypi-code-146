#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from copy import deepcopy
from dataclasses import dataclass
from typing import Type

import numpy as np
import pytest

from pyxel.detectors import CCDGeometry, CMOSGeometry, Geometry


@dataclass
class Parameters:
    """Only for testing."""

    row: int
    col: int
    pixel_vert_size: float
    pixel_horz_size: float


@pytest.mark.parametrize("geometry_cls", [CCDGeometry, CMOSGeometry])
@pytest.mark.parametrize(
    "parameters, exp_values",
    [
        pytest.param(
            Parameters(row=3, col=2, pixel_vert_size=0.1, pixel_horz_size=0.2),
            np.array([0.05, 0.05, 0.15, 0.15, 0.25, 0.25]),
            id="3x2",
        ),
        pytest.param(
            Parameters(row=3, col=1, pixel_vert_size=0.1, pixel_horz_size=0.2),
            np.array([0.05, 0.15, 0.25]),
            id="3x1",
        ),
        pytest.param(
            Parameters(row=1, col=3, pixel_vert_size=0.1, pixel_horz_size=0.2),
            np.array([0.05, 0.05, 0.05]),
            id="1x3",
        ),
    ],
)
def test_vertical_pixel_center_pos(
    geometry_cls: Type[Geometry], parameters: Parameters, exp_values: np.ndarray
):
    """Test method '.vertical_pixel_center_pos_list'."""
    # Create the geometry object
    geometry = geometry_cls(
        row=parameters.row,
        col=parameters.col,
        pixel_vert_size=parameters.pixel_vert_size,
        pixel_horz_size=parameters.pixel_horz_size,
    )

    # Get the positions
    values = geometry.vertical_pixel_center_pos_list()

    # Check the positions
    np.testing.assert_allclose(values, exp_values)


@pytest.mark.parametrize("geometry_cls", [CCDGeometry, CMOSGeometry])
@pytest.mark.parametrize(
    "parameters, exp_values",
    [
        pytest.param(
            Parameters(row=3, col=2, pixel_vert_size=0.1, pixel_horz_size=0.2),
            np.array([0.1, 0.3, 0.1, 0.3, 0.1, 0.3]),
            id="3x2",
        ),
        pytest.param(
            Parameters(row=3, col=1, pixel_vert_size=0.1, pixel_horz_size=0.2),
            np.array([0.1, 0.1, 0.1]),
            id="3x1",
        ),
        pytest.param(
            Parameters(row=1, col=3, pixel_vert_size=0.1, pixel_horz_size=0.2),
            np.array([0.1, 0.3, 0.5]),
            id="1x3",
        ),
    ],
)
def test_horizontal_pixel_center_pos(
    geometry_cls: Type[Geometry], parameters: Parameters, exp_values: np.ndarray
):
    """Test method '.horizontal_pixel_center_pos_list'."""
    # Create the geometry object
    geometry = geometry_cls(
        row=parameters.row,
        col=parameters.col,
        pixel_vert_size=parameters.pixel_vert_size,
        pixel_horz_size=parameters.pixel_horz_size,
    )

    # Get the positions
    values = geometry.horizontal_pixel_center_pos_list()

    np.testing.assert_allclose(values, exp_values)


@pytest.mark.parametrize(
    "row, col, total_thickness, pixel_vert_size, pixel_horz_size",
    [(1, 1, 0.0, 0.0, 0.0), (10000, 10000, 10000.0, 1000.0, 1000.0)],
)
def test_create_valid_geometry(
    row, col, total_thickness, pixel_vert_size, pixel_horz_size
):
    """Test when creating a valid `Geometry` object."""
    _ = Geometry(
        row=row,
        col=col,
        total_thickness=total_thickness,
        pixel_vert_size=pixel_vert_size,
        pixel_horz_size=pixel_horz_size,
    )


@pytest.mark.parametrize(
    "row, col, total_thickness, pixel_vert_size, pixel_horz_size, exp_exc",
    [
        pytest.param(0, 100, 100.0, 100.0, 100.0, ValueError, id="row == 0"),
        pytest.param(-1, 100, 100.0, 100.0, 100.0, ValueError, id="row < 0"),
        pytest.param(100, 0, 100.0, 100.0, 100.0, ValueError, id="col == 0"),
        pytest.param(100, -1, 100.0, 100.0, 100.0, ValueError, id="col < 0"),
        pytest.param(
            100, 100, -0.1, 100.0, 100.0, ValueError, id="total_thickness < 0."
        ),
        pytest.param(
            100, 100, 10000.1, 100.0, 100.0, ValueError, id="total_thickness > 10000."
        ),
    ],
)
def test_create_invalid_geometry(
    row, col, total_thickness, pixel_vert_size, pixel_horz_size, exp_exc
):
    """Test when creating an invalid `Geometry` object."""
    with pytest.raises(exp_exc):
        _ = Geometry(
            row=row,
            col=col,
            total_thickness=total_thickness,
            pixel_vert_size=pixel_vert_size,
            pixel_horz_size=pixel_horz_size,
        )


@pytest.mark.parametrize(
    "other_obj, is_equal",
    [
        pytest.param(None, False, id="None"),
        pytest.param(Geometry(row=100, col=120), False, id="Only two parameters"),
        pytest.param(
            Geometry(
                row=100,
                col=120,
                total_thickness=123.1,
                pixel_horz_size=12.4,
                pixel_vert_size=34.5,
            ),
            True,
            id="Same parameters, same class",
        ),
        pytest.param(
            CCDGeometry(
                row=100,
                col=120,
                total_thickness=123.1,
                pixel_horz_size=12.4,
                pixel_vert_size=34.5,
            ),
            False,
            id="Same parameters, different class",
        ),
    ],
)
def test_is_equal(other_obj, is_equal):
    """Test equality statement for Geometry."""
    obj = Geometry(
        row=100,
        col=120,
        total_thickness=123.1,
        pixel_horz_size=12.4,
        pixel_vert_size=34.5,
    )

    if is_equal:
        assert obj == other_obj
    else:
        assert obj != other_obj


@pytest.mark.parametrize(
    "obj, exp_dict",
    [
        (
            Geometry(
                row=100,
                col=120,
                total_thickness=123.1,
                pixel_horz_size=12.4,
                pixel_vert_size=34.5,
            ),
            {
                "row": 100,
                "col": 120,
                "total_thickness": 123.1,
                "pixel_horz_size": 12.4,
                "pixel_vert_size": 34.5,
            },
        ),
    ],
)
def test_to_and_from_dict(obj, exp_dict):
    """Test methods 'to_dict', 'from_dict'."""
    assert type(obj) == Geometry

    # Convert from `Geometry` to a `dict`
    dct = obj.to_dict()
    assert dct == exp_dict

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    assert copied_dct == exp_dict

    # Convert from `dict` to `Geometry`
    other_obj = Geometry.from_dict(copied_dct)
    assert type(other_obj) == Geometry
    assert obj == other_obj
    assert obj is not other_obj
    assert copied_dct == exp_dict
