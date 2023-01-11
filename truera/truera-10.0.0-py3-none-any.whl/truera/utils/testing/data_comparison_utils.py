from typing import Union
import unittest

import numpy as np
import pandas as pd


def _updateOrReadData(
    actual_data: Union[pd.DataFrame, np.ndarray],
    expected_data_filename: str,
    update_file: bool = False
) -> pd.DataFrame:
    if update_file:
        if isinstance(actual_data, np.ndarray):
            actual_data = pd.DataFrame(data=actual_data)
        actual_data.to_csv(expected_data_filename, index=None)
    return pd.read_csv(expected_data_filename)


def assertDataEqualsWithTestCase(
    test_case: unittest.TestCase,
    actual_data: Union[pd.DataFrame, np.ndarray],
    expected_data_filename: str,
    update_file: bool = False,
    check_names: bool = True
):
    assertDataAlmostEqualsWithTestCase(
        test_case,
        actual_data,
        expected_data_filename,
        atol=0,
        rtol=0,
        update_file=update_file,
        check_names=check_names
    )


def assertDataAlmostEqualsWithTestCase(
    test_case: unittest.TestCase,
    actual_data: Union[pd.DataFrame, np.ndarray],
    expected_data_filename: str,
    atol: float = 1e-3,
    rtol: float = 1e-3,
    update_file: bool = False,
    check_names: bool = True
):
    expected_data = _updateOrReadData(
        actual_data, expected_data_filename, update_file=update_file
    )
    if update_file:
        test_case.fail("Test in record mode. (update_file=True)")
    if isinstance(actual_data, pd.DataFrame):
        pd.testing.assert_frame_equal(
            actual_data,
            expected_data,
            atol=atol,
            rtol=rtol,
            check_names=check_names
        )
    elif isinstance(actual_data, pd.Series):
        pd.testing.assert_series_equal(
            actual_data,
            expected_data[expected_data.columns[0]],
            atol=atol,
            rtol=rtol,
            check_names=check_names
        )

    elif isinstance(actual_data, np.ndarray):
        test_case.assertTrue(
            np.allclose(
                actual_data.ravel(),
                expected_data.to_numpy().ravel(),
                atol=atol,
                rtol=rtol
            )
        )
    else:
        raise TypeError(
            f"actual_data must be one of [pandas.DataFrame, numpy.ndarray] but given {type(actual_data)}!"
        )
