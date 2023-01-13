#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from pathlib import Path
from typing import Optional

from colorama import Fore
from colorama import Style
from google.api_core.exceptions import BadRequest
from google.cloud.bigquery import Client as bqclient


class BigQueryConnector:
    """Provides BigQuery Connector to extracts data from bigquery database."""

    _conn: Optional[bqclient] = None

    def __init__(
        self,
        bigquery_credential_path: str,
        query: str,
        output: str = "local",
        file_name: Optional[str] = "",
        file_path: Optional[str] = "",
    ):
        """
        Connect with bigquery database, fetch data from bigquery and store into your output path.

        Args:
            bigquery_credential (str): bigquery service account credentials path
            query (str): query to retrieve data
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None
        """
        self._json_cred = bigquery_credential_path
        self._query = query
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

    def _get_bigquery_reg_conn(self):
        """Creates a connection to the bigquery database."""

        if not self._conn:
            self._conn = bqclient.from_service_account_json(
                json_credentials_path=self._json_cred
            )

        return self._conn

    def __get_df(self):
        """
        This function will extracts data from bigquery database.

        Returns:
            DataFrame
        """
        try:
            _conn = self._get_bigquery_reg_conn()
            print("Connection to bigquery stablished Successfully.")
            self._query_job = _conn.query(self._query)
        except BadRequest as e:
            for e in self._query_job.errors:
                print(f"ERROR: {e['message']}")
        else:
            self.fname = f"biquery_{self._file_name or self._query_job.destination.project}_{self._query_job.created.strftime('%Y_%m_%d_%H_%M_%S')}.csv"
            self._dstn_path = f"{self._dst_path}/{self.fname}"
            return self._query_job.to_dataframe()

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
