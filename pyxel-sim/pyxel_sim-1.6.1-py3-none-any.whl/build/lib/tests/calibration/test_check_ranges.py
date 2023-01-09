#  Copyright (c) European Space Agency, 2017, 2018, 2019, 2020, 2021, 2022.
#
#  This file is subject to the terms and conditions defined in file 'LICENCE.txt', which
#  is part of this Pyxel package. No part of the package, including
#  this file, may be copied, modified, propagated, or distributed except according to
#  the terms contained in the file ‘LICENCE.txt’.

from typing import Optional

import pytest

from pyxel.calibration.util import check_ranges


@pytest.mark.parametrize(
    "target_range, out_range, rows, cols, readout_times",
    [
        # Nothing to check
        ([], [], 10, 10, None),
        ([0, 5, 0, 10], [], 5, 10, None),  # No 'readout_times'
        # 2D : (start_row, stop_row, start_col, stop_col)
        ([0, 5, 0, 10], [0, 5, 0, 10], 5, 10, None),  # No 'readout_times'
        ([0, 10, 0, 5], [0, 10, 0, 5], 10, 5, None),  # No 'readout_times'
        ([0, 5, 0, 10], [10, 15, 10, 20], 5, 10, None),  # No 'readout_times'
        ([0, 5, 0, 10], [0, 5, 0, 10], 5, 10, -1),  # Lowest 'readout_times'
        ([0, 5, 0, 10], [0, 5, 0, 10], 5, 10, 100),  # Highest 'readout_times'
        # 3D : (start_time, stop_time, start_row, stop_row, start_col, stop_col)
        (
            [0, 5, 0, 10, 0, 20],
            [0, 5, 0, 10, 0, 20],
            10,
            20,
            5,
        ),  # No 'readout_times'
        (
            [0, 5, 0, 20, 0, 10],
            [0, 5, 0, 20, 0, 10],
            20,
            10,
            5,
        ),  # No 'readout_times'
        (
            [0, 5, 0, 10, 0, 20],
            [0, 5, 30, 40, 50, 70],
            10,
            20,
            5,
        ),  # No 'readout_times'
        (
            [0, 5, 20, 40, 0, 10],
            [0, 5, 0, 20, 0, 10],
            40,
            10,
            5,
        ),  # No 'readout_times'
    ],
)
def test_check_range_valid(
    target_range: list,
    out_range: list,
    rows: int,
    cols: int,
    readout_times: Optional[int],
):
    """Test valid values for function 'check_range'."""
    check_ranges(
        target_fit_range=target_range,
        out_fit_range=out_range,
        rows=rows,
        cols=cols,
        readout_times=readout_times,
    )


@pytest.mark.parametrize(
    "target_range, out_range, rows, cols, readout_times, exp_error",
    [
        # 'target_range' is neither 2D nor 3D
        pytest.param([0], [0, 5, 0, 10], 5, 10, None, "", id="Target 1 element"),
        pytest.param([0, 5], [0, 5, 0, 10], 5, 10, None, "", id="Target 2 elements"),
        pytest.param([0, 5, 0], [0, 5, 0, 10], 5, 10, None, "", id="Target 3 elements"),
        pytest.param(
            [0, 5, 10, 0, 5], [0, 5, 0, 10], 5, 10, None, "", id="Target 5 elements"
        ),
        # 'out_range' is neither 2D nor 3D
        pytest.param([0, 5, 0, 10], [0], 5, 10, None, "", id="Out 1 element"),
        pytest.param([0, 5, 0, 10], [0, 5], 5, 10, None, "", id="Out 2 element"),
        pytest.param([0, 5, 0, 10], [0, 5, 0], 5, 10, None, "", id="Out 3 element"),
        pytest.param(
            [0, 5, 0, 10], [0, 5, 0, 10, 11], 5, 10, None, "", id="Out 5 element"
        ),
        # 2D : (start_row, stop_row, start_col, stop_col)
        # Different span for 'target_range' and 'out_range'
        pytest.param(
            [0, 5, 0, 10],
            [0, 6, 0, 10],
            5,
            10,
            None,
            "Fitting ranges have different lengths in 1st dimension",
            id="1D length - too long",
        ),
        pytest.param(
            [0, 5, 0, 10],
            [1, 5, 0, 10],
            5,
            10,
            None,
            "Fitting ranges have different lengths in 1st dimension",
            id="1D length - too short",
        ),
        pytest.param(
            [0, 5, 0, 10],
            [0, 5, 0, 11],
            5,
            10,
            None,
            "Fitting ranges have different lengths in 2nd dimension",
            id="2D length - too long",
        ),
        pytest.param(
            [0, 5, 0, 10],
            [0, 5, 0, 9],
            5,
            10,
            None,
            "Fitting ranges have different lengths in 2nd dimension",
            id="2D length - too short",
        ),
        # 3D : (start_time, stop_time, start_row, stop_row, start_col, stop_col)
        pytest.param(
            [0, 5, 0, 10, 0, 20],
            [0, 5, 0, 10, 0, 19],
            5,
            10,
            5,
            "Fitting ranges have different lengths in third dimension",
            id="3D length - too short",
        ),
        pytest.param(
            [0, 5, 0, 10, 0, 20],
            [0, 5, 0, 10, 0, 21],
            5,
            10,
            5,
            "Fitting ranges have different lengths in third dimension",
            id="3D length - too long",
        ),
        pytest.param(
            [0, 5, 0, 10, 0, 20],
            [0, 5, 0, 10, 0, 20],
            9,  # Too low
            20,
            20,
            "Value of target fit range is wrong",
            id="3D length - wrong target row range1",
        ),
        pytest.param(
            [0, 5, 30, 40, 0, 20],
            [0, 5, 30, 40, 0, 20],
            29,  # too low
            10,
            20,
            "Value of target fit range is wrong",
            id="3D length - wrong target row range2",
        ),
        pytest.param(
            [0, 5, 0, 10, 0, 20],
            [0, 5, 0, 10, 0, 20],
            10,
            19,
            5,
            "Value of target fit range is wrong",
            id="3D length - wrong target col range1",
        ),
        pytest.param(
            [0, 5, 0, 10, 20, 40],
            [0, 5, 0, 10, 0, 20],
            10,
            39,  # too low
            5,
            "Value of target fit range is wrong",
            id="3D length - wrong target col range2",
        ),
        pytest.param(
            [0, 5, 0, 10, 20, 40],
            [0, 5, 0, 10, 0, 20],
            10,
            19,  # too low
            5,
            "Value of target fit range is wrong",
            id="3D length - wrong target col range3",
        ),
        pytest.param(
            [0, 5, 0, 10, 0, 20],
            [0, 5, 0, 10, 0, 20],
            10,
            20,
            None,
            "Target data is not a 3 dimensional array",
            id="3D length - Missing 'readout_times'",
        ),
        pytest.param(
            [10, 15, 0, 10, 0, 20],
            [10, 15, 0, 10, 0, 20],
            10,
            20,
            14,  # too low
            "Value of target fit range is wrong",
            id="3D length - wrong target time range1",
        ),
        pytest.param(
            [10, 15, 0, 10, 0, 20],
            [10, 15, 0, 10, 0, 20],
            10,
            20,
            9,  # too low
            "Value of target fit range is wrong",
            id="3D length - wrong target time range2",
        ),
    ],
)
def test_check_ranges_invalid(
    target_range: list,
    out_range: list,
    rows: int,
    cols: int,
    readout_times: Optional[int],
    exp_error,
):
    """Test valid values for function 'check_range'."""
    with pytest.raises(ValueError, match=exp_error):
        check_ranges(
            target_fit_range=target_range,
            out_fit_range=out_range,
            rows=rows,
            cols=cols,
            readout_times=readout_times,
        )
