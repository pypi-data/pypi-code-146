#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from pathlib import Path
from time import gmtime
from time import strftime
from typing import Optional

import hana_ml.dataframe as dataframe
from colorama import Fore
from colorama import Style


class SAPHANAConnector:
    """Provides SAP HANA Connector to extracts data from sap hana database."""

    _conn: Optional[dataframe.ConnectionContext] = None

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        table_name: str,
        schema: str,
        query: Optional[str],
        output: str = "local",
        file_name: Optional[str] = "",
        file_path: Optional[str] = "",
    ):
        """
        Connect with SAP HANA database, fetch data from sap hana and store into your output path.

        Args:
            host (str): database host address
            port (int): connection port number
            user (str): sap hana user name used to authenticate
            password (str): password used to authenticate
            table_name (str): table name from where you want retrieve data
            schema (str): database schema name
            query (str): custom query to retrieve data
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None

        """
        self._host_address = host
        self._user = user
        self._port = port
        self._password = password
        self._table_name = table_name
        self._schema = schema
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

    def _get_sap_hana_reg_conn(self):
        """Creates a connection to the sap hana database."""

        if not self._conn:
            self._conn = dataframe.ConnectionContext(
                address=self._host_address,
                port=self._port,
                user=self._user,
                password=self._password,
            )

        return self._conn

    def __get_df(self):
        """
        This function will extracts data from sap hana database.

        Returns:
            DataFrame
        """
        self.fname = f"sap_hana_{self._schema}_{self._file_name or self._table_name}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dstn_path = f"{self._dst_path}/{self.fname}"

        _conn = self._get_sap_hana_reg_conn()
        if not _conn.connection.isconnected():
            print("Failed to Establish Connection")

        print("Connection to SAP HANA stablished Successfully.")

        if not self._custom_query:
            self._custom_query = f"SELECT * FROM {self._schema}.{self._table_name}"

        return dataframe.DataFrame(_conn, self._custom_query).collect()

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
