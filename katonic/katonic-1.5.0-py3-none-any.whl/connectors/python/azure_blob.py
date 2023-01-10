#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from io import StringIO
from pathlib import Path
from time import gmtime
from time import strftime
from typing import Optional

import pandas as pd
from azure.storage.blob import BlockBlobService
from colorama import Fore
from colorama import Style


class AzureBlobConnector:
    """Provides Azure Blob Connector to extracts data from azure blob storage."""

    _blob_service: Optional[BlockBlobService] = None

    def __init__(
        self,
        account_name: str = "",
        account_key: str = "",
        container_name: str = "",
        blob_name: str = "",
        output: str = "local",
        file_name: Optional[str] = "",
        file_path: Optional[str] = "",
    ):
        """
        Connect with azure blob database, fetch data from azure and store into your output path.

        Args:
            account_name (str): storage account name to authenticate requests signed with
            an account key and to construct the storage endpoint
            account_key (str): storage account key for shared key authentication
            container_name (str): name of existing container
            blob_name (str): name of existing blob
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None
        """
        self._account_name = account_name
        self._account_key = account_key
        self._container_name = container_name
        self._blob_name = blob_name
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

    def _get_azure_reg_conn(self):
        """Creates a connection to the azure blob."""

        if not self._blob_service:
            self._blob_service = BlockBlobService(
                account_name=self._account_name, account_key=self._account_key
            )

        return self._blob_service

    def __get_df(self):
        """
        This function will extracts data from azure blob storage.

        Returns:
            DataFrame
        """
        self.fname = f"azure_{self._container_name}_{self._file_name or self._blob_name.split('.')[0]}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dstn_path = f"{self._dst_path}/{self.fname}"

        try:
            _conn = self._get_azure_reg_conn()
            print("Connection instance to azure blob storage stablished Successfully.")
        except Exception as e:
            raise ValueError("Connection to azure blob storage failed.") from e
        else:
            _data_string = _conn.get_blob_to_text(
                self._container_name, self._blob_name, encoding="latin1"
            ).content
            return pd.read_csv(StringIO(_data_string))

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
