#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#
from pathlib import Path
from time import gmtime
from time import strftime
from typing import Optional

import snowflake.connector
from colorama import Fore
from colorama import Style


class SnowFlakeConnector:
    """Provides Snowflake Connector to extracts data from snowflake database."""

    _conn: Optional[snowflake.connector.connect] = None

    def __init__(
        self,
        user: str,
        password: str,
        account: str,
        database: str,
        table_name: str,
        schema: str,
        warehouse: str = "",
        query: Optional[str] = "",
        output: str = "local",
        file_name: Optional[str] = "",
        file_path: Optional[str] = "",
    ):
        """
        Connect with snowflake, fetch data from snowflake and store into your output path.

        Args:
            user (str): login name for the user to authenticate
            password (str): password for the user to authenticate
            account (str): your account identifier
            database (str): name of the default database to use
            table_name (str): table name from where you want retrieve data
            schema (str): name of the default schema to use for the database
            warehouse (int): name of the default warehouse to use
            query (Optional[str]): custom query to retrieve data
            output (Optional[str]): output type, it can be `local` or `katonic` (default: `local` if not provided)
            file_name (Optional[str]): output file name on which retrieved data will be stored
            file_path (Optional[str]): output path where you want to store data

        Returns:
            None
        """
        self._user = user
        self._password = password
        self._account = account
        self._warehouse = warehouse
        self._database = database
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

    def _get_snowflake_reg_conn(self):
        """Creates a connection to the snowflake database."""

        if not self._conn:

            self._conn = snowflake.connector.connect(
                user=self._user,
                password=self._password,
                account=self._account,
            )

        return self._conn

    def __get_df(self):
        """
        This function will extracts data from snowflake database.

        Returns:
            DataFrame
        """

        self.fname = f"snowflake_{self._schema}_{self._database}_{self._file_name or self._table_name}_{strftime('%Y_%m_%d_%H_%M_%S', gmtime())}.csv"
        self._dstn_path = f"{self._dst_path}/{self.fname}"

        if not self._custom_query:
            self._custom_query = f"SELECT * FROM {self._schema}.{self._table_name};"

        try:
            _conn = self._get_snowflake_reg_conn()
            _cur = _conn.cursor()

            if self._warehouse:
                try:
                    _cur.execute(f"USE WAREHOUSE {self._warehouse}")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)

            if self._database:
                try:
                    _cur.execute(f"USE DATABASE {self._database}")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)

            if self._schema:
                try:
                    _cur.execute(f"USE SCHEMA {self._schema}")
                except snowflake.connector.errors.ProgrammingError as e:
                    print(e)

            print("Connection to snowflake stablished Successfully.")

        except snowflake.connector.errors.ProgrammingError as e:
            print(f"Error {e.errno} ({e.sqlstate}): {e.msg} ({e.sfqid})")
        else:
            try:
                _cur.execute(self._custom_query)
            except snowflake.connector.errors.ProgrammingError as e:
                print(e)
            else:
                # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
                return _cur.fetch_pandas_all()
            # finally:
            #     _cur.close()
            #     _conn.close()

    def get_data(self):
        """
        This function saves the data into csv file.

        Returns:
            None

        Raises:
            ValueError: if output type provided other than `local` or `katonic`."""
        try:
            # Fetch the result set from the cursor and deliver it as the Pandas DataFrame.
            _data = self.__get_df()
            _data.to_csv(self._dstn_path, index=False)
            print(
                f"File saved to your {Style.BRIGHT + Fore.GREEN}'{self._output}'{Style.RESET_ALL}"
                f"file system with name {Style.BRIGHT + Fore.GREEN}'{self.fname}'{Style.RESET_ALL} Successfully."
            )
        except Exception as exc:
            raise ValueError(
                f"Failed to save data to your {Style.BRIGHT + Fore.RED}'{self._output}'{Style.RESET_ALL} file system path."
            ) from exc

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
