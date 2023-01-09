#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from copy import deepcopy

import pytest

from pyxel.detectors import CCDGeometry, Geometry


@pytest.mark.parametrize(
    "row, col, total_thickness, pixel_vert_size, pixel_horz_size",
    [(1, 1, 0.0, 0.0, 0.0), (10000, 10000, 10000.0, 1000.0, 1000.0)],
)
def test_create_valid_geometry(
    row, col, total_thickness, pixel_vert_size, pixel_horz_size
):
    """Test when creating a valid `Geometry` object."""
    _ = CCDGeometry(
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
        _ = CCDGeometry(
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
        pytest.param(CCDGeometry(row=100, col=120), False, id="Only two parameters"),
        pytest.param(
            CCDGeometry(
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
            Geometry(
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
    """Test equality statement for CCDGeometry."""
    obj = CCDGeometry(
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
            CCDGeometry(
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
    assert type(obj) == CCDGeometry

    # Convert from `CCDGeometry` to a `dict`
    dct = obj.to_dict()
    assert dct == exp_dict

    # Copy 'exp_dict'
    copied_dct = deepcopy(exp_dict)  # create a new dict
    assert copied_dct is not exp_dict
    assert copied_dct == exp_dict

    # Convert from `dict` to `CCDGeometry`
    other_obj = CCDGeometry.from_dict(copied_dct)
    assert type(other_obj) == CCDGeometry
    assert obj == other_obj
    assert obj is not other_obj
    assert copied_dct == exp_dict
