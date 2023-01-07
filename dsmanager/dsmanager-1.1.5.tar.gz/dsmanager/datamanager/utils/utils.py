"""@Author: Rayane AMROUCHE

Utils for DataManager.
"""

import os

from typing import Any

import pandas as pd  # type: ignore

from dotenv import load_dotenv  # type: ignore

from dsmanager.controller.logger import make_logger

from dsmanager.datamanager.utils._dataframe import DataFrameUtils
from dsmanager.datamanager.utils._column import ColumnUtils
from dsmanager.datamanager.utils._plotting import PlottingUtils

from dsmanager.datamanager.utils import _pandas_object


class Utils:
    """Utils class brings utils tools for the data manager."""

    def __init__(
        self, __dm: Any, logger_path: str = "/tmp/logs", verbose: int = 0
    ) -> None:
        """Init class Utils with an empty local storage.

        Args:
            __dm (Any): DataManager from which these utils are called.
            logger_path (str, optional): Path of the logger for the DataManager.
                Defaults to "/tmp/logs".
            verbose (int, optional): Verbose level for the logger . Defaults to 0.
        """
        self.__dm = __dm
        self.logger = make_logger(
            os.path.join(logger_path, "datamanager"), "utils", verbose=verbose
        )

        self.column = ColumnUtils()
        self.dataframe = DataFrameUtils()
        self.plot = PlottingUtils()

    def copy_as(self, df_: pd.DataFrame, name: str) -> pd.DataFrame:
        """Copy a pandas DataFrame in the datamanager with a given name.

        Args:
            df_ (pd.DataFrame): DataFrame to save.
            name (str): Alias of the DataFrame in the DataStorage of the DataManager.

        Returns:
            pd.DataFrame: Returns original DataFrame to keep chaining.
        """
        self.__dm.datas[name] = df_
        return df_

    def load_env(
        self,
        env_path: str = "",
    ) -> None:
        """Load env file from a given path or from the datamanager.

        Args:
            env_path (str, optional): Path of the env file. Defaults to "".
        """
        if env_path:
            load_dotenv(env_path)


pd.core.base.PandasObject.to_datamanager = _pandas_object.to_datamanager
pd.core.base.PandasObject.pipe_sklearn = _pandas_object.pipe_sklearn
pd.core.base.PandasObject.pipe_leaf = _pandas_object.pipe_leaf
pd.core.base.PandasObject.pipe_steps = _pandas_object.pipe_steps
