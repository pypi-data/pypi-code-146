"""Module containing CSVSource class.

CSVSource class handles loading of CSV data.
"""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, Iterable, List, Optional, Union

import methodtools
import numpy as np
import pandas as pd
from pydantic import AnyUrl

from bitfount.data.datasources.base_source import BaseSource
from bitfount.types import _Dtypes
from bitfount.utils import delegates

logger = logging.getLogger(__name__)


@delegates()
class CSVSource(BaseSource):
    """Data source for loading csv files.

    Args:
        path: The path or URL to the csv file.
        read_csv_kwargs: Additional arguments to be passed as a
            dictionary to `pandas.read_csv`. Defaults to None.
    """

    def __init__(
        self,
        path: Union[os.PathLike, AnyUrl, str],
        read_csv_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        if not str(path).endswith(".csv"):
            raise TypeError("Please provide a Path or URL to a CSV file.")
        self.path = str(path)
        if not read_csv_kwargs:
            read_csv_kwargs = {}
        self.read_csv_kwargs = read_csv_kwargs

    # TODO: [BIT-1780] Simplify referencing data in here and in other sources
    # We want to avoid recalculating but we dont want to cache more
    # than one result at a time to save memory
    @methodtools.lru_cache(maxsize=1)
    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns data from CSV dataset.

        Returns:
            A DataFrame-type object which contains the data.
        """
        csv_df: pd.DataFrame = pd.read_csv(self.path, **self.read_csv_kwargs)
        return csv_df

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in CSV dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.

        """
        return {col: self.get_data(**kwargs)[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from CSV dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        csv_df: pd.DataFrame = self.get_data(**kwargs)
        return csv_df[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types of the CSV dataset.

        Returns:
            A mapping from column names to column types.
        """
        csv_df: pd.DataFrame = self.get_data(**kwargs)
        return self._get_data_dtypes(csv_df)

    def __len__(self) -> int:
        return len(self.get_data())
