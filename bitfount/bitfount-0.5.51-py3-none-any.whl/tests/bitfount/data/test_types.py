"""Tests types.py."""
from datetime import datetime
import string
from typing import Literal, Union

import numpy as np
from numpy.testing import assert_array_equal
import pandas as pd
import pytest

from bitfount.data.types import _ExtendableLabelEncoder
from tests.utils.helper import create_dataset, unit_test


@unit_test
class TestExtendableLabelEncoder:
    """Tests the extendable label encoder."""

    DATA = np.array(list(string.ascii_lowercase))
    DATA2 = np.array(list(str(x) for x in range(0, 10)))

    def test_add_values(self) -> None:
        """Checks we can successfully add values.

        Also checks we don't get extras if doing it twice.
        """
        len1 = len(self.DATA)
        len2 = len(self.DATA2)
        encoder = _ExtendableLabelEncoder()
        encoder.add_values(self.DATA)
        assert encoder.size == len1
        encoder.add_values(self.DATA)
        assert encoder.size == len1
        encoder.add_values(self.DATA2)
        assert encoder.size == len1 + len2

    def test_transform_str(self) -> None:
        """Checks we can encode a column that is strings."""
        encoder = _ExtendableLabelEncoder()
        encoder.add_values(self.DATA)
        encoder.add_values(self.DATA2)
        input_arr = pd.Series(["a", "0", "2", "b"])
        encoded = encoder.transform(input_arr)
        assert_array_equal(encoded, np.array([0, 26, 28, 1]))

    def test_transform_error(self) -> None:
        """Tests transform error."""
        encoder = _ExtendableLabelEncoder()
        encoder.add_values(self.DATA)
        encoder.add_values(self.DATA2)
        with pytest.raises(ValueError):
            encoder.transform(pd.Series(["a", "a", "0", "2", "unseen"]))

    def test_size(self) -> None:
        """Tests size property explicitly."""
        encoder = _ExtendableLabelEncoder()
        encoder.classes = dict(zip(["a", "b", "c"], [1, 2, 3]))
        assert encoder.size == 3

    def test_eq_magic_method(self) -> None:
        """Tests that __eq__ works as expected."""
        encoder1 = _ExtendableLabelEncoder()
        encoder1.add_values(self.DATA)
        encoder2 = _ExtendableLabelEncoder()
        encoder2.add_values(self.DATA2)
        encoder3 = _ExtendableLabelEncoder()
        encoder3.add_values(self.DATA)
        assert not (encoder1 == encoder2)
        assert encoder1 == encoder3

    @pytest.mark.parametrize("values_type", ["pandas", "numpy"])
    def test_date_column(
        self, values_type: Union[Literal["pandas"], Literal["numpy"]]
    ) -> None:
        """Tests that encoding with a date column works."""
        dataframe = create_dataset()
        date_column = dataframe["Date"]
        encoder = _ExtendableLabelEncoder()
        if values_type == "pandas":
            encoder.add_values(date_column)
        else:
            # Adds just the unique values as a numpy array
            encoder.add_values(np.asarray(date_column.unique()))
        transformed_column = encoder.transform(date_column)
        assert sorted(set(transformed_column)) == sorted(encoder.classes.values())

    @pytest.mark.parametrize("values_type", ["pandas", "numpy"])
    def test_datetime_column(
        self, values_type: Union[Literal["pandas"], Literal["numpy"]]
    ) -> None:
        """Tests that encoding with a datetime column works."""
        dataframe = create_dataset()
        dataframe["Date"] = datetime(2020, 1, 1, 11, 30, 15)
        date_column = dataframe["Date"]
        encoder = _ExtendableLabelEncoder()
        if values_type == "pandas":
            encoder.add_values(date_column)
        else:
            # Adds just the unique values as a numpy array
            encoder.add_values(np.asarray(date_column.unique()))
        transformed_column = encoder.transform(date_column)
        assert sorted(set(transformed_column)) == sorted(encoder.classes.values())

    @pytest.mark.parametrize("values_type", ["pandas", "numpy"])
    def test_datetime_column_with_empty_time(
        self, values_type: Union[Literal["pandas"], Literal["numpy"]]
    ) -> None:
        """Tests that encoding with a datetime column with no time works."""
        dataframe = create_dataset()
        dataframe["Date"] = datetime(2020, 1, 1)
        date_column = dataframe["Date"]
        encoder = _ExtendableLabelEncoder()
        if values_type == "pandas":
            encoder.add_values(date_column)
        else:
            # Adds just the unique values as a numpy array
            encoder.add_values(np.asarray(date_column.unique()))
        transformed_column = encoder.transform(date_column)
        assert sorted(set(transformed_column)) == sorted(encoder.classes.values())
