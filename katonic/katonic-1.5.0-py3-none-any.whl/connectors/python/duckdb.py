#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from pathlib import Path
from time import gmtime
from time import strftime
from typing import Optional

import duckdb
from colorama import Fore
from colorama import Style


class DuckDBConnector:
    """Provides DuckDB Connector to extracts data from duckdb database."""

    _conn: Optional[duckdb.connect] = None

    def __init__(
        self,
        database: str,
        query: str,
        output: str = "local",
        file_name: Optional[str] = "",
        file_path: Optional[str] = "",
    ):
        """
        Connect with duckdb database, fetch data from duckdb and store into your output path.

        Args:
            database (str): database name eg: example.duckdb
            query (str): custom query to retrieve data
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None

        """
        self._db_name = database
        self._custom_query = query
        self._output = output
        self._file_name = file_name
        self._file_path = file_path
        self.fname = ""

        if self._output.lower() == "local":
            Path(self._file_path).mkdir(
                parents=True, exist_ok=True
            ) if self._file_path else ""
            self._dst_path = (
                Path(self._file_path).absolute()
                if self._file_path
                else Path().absolute()
            )
        elif self._output.lower() == "katonic":
            if self._file_path:
                Path(f"/kfs_private/{self._file_path}").mkdir(
                    parents=True, exist_ok=True
                )
                self._dst_path = Path(f"/kfs_private/{self._file_path}").absolute()
            else:
                self._dst_path = Path("/kfs_private/").absolute()
        else:
            raise ValueError(
                f"invalid literal for variable output: '{self._output}', it must be one from 'local' or 'katonic'."
            )

    def _get_duckdb_reg_conn(self):
        """Creates a connection to the duckdb database."""

        if not self._conn:
            self._conn = duckdb.connect(
                database=self._db_name,
                read_only=True,
            )

        return self._conn

    def __get_df(self):
        """
        This function will extracts data from duckdb database.

        Returns:
            DataFrame
        """
        fname = f"duckdb_{self._db_name.split('.')[0]}_{self._file_name}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dstn_path = f"{self._dst_path}/{fname}"

        _conn = self._get_duckdb_reg_conn()
        print("Connection to duckdb stablished Successfully.")

        return _conn.execute(self._custom_query).fetchdf()

    def get_data(self):
        """
        This function saves the data into csv file.

        Returns:
            None

        Raises:
            ValueError: if output type provided other than `local` or `katonic`."""
        try:
            _data = self.__get_df()
            _data.to_csv(self._dstn_path, index=False)
            print(
                f"File saved to your {Style.BRIGHT + Fore.GREEN}'{self._output}'{Style.RESET_ALL}"
                f"file system with name {Style.BRIGHT + Fore.GREEN}'{self.fname}'{Style.RESET_ALL} Successfully."
            )
        except Exception as e:
            raise ValueError(
                f"Failed to save data to your {Style.BRIGHT + Fore.RED}'{self._output}'{Style.RESET_ALL} file system path."
            ) from e

    def to_df(self):
        """Returns the retrieved dataframe from database."""
        return self.__get_df()

    @property
    def file_name(self) -> str:
        """Gets the generated output filename."""
        if not self.fname:
            import warnings

            warnings.warn(
                ("First run the `get_data` function to get the output filename."),
                category=UserWarning,
                stacklevel=2,
            )
        return self.fname
