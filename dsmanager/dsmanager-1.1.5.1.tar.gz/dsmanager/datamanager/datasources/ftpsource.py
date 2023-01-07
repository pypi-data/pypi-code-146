"""@Author: Rayane AMROUCHE

Ftp Sources Handling.
"""

import os
import json
import urllib.request

from contextlib import closing
from typing import Any

from dsmanager.datamanager.datasources.datasource import DataSource
from dsmanager.datamanager.utils import find_type


class FtpSource(DataSource):
    """Inherited Data Source Class for ftp sources."""

    @staticmethod
    def show_schema() -> None:
        """Get source metadata schema."""
        ftp_schema = {
            "source_type": "ftp",
            "server": "ftp_server_address",
            "port": 21,
            "username_env_name": "server_username_environment_variable_name",
            "password_env_name": "server_password_environment_variable_name",
        }
        ftp_schema.update(DataSource.file_schema())
        print(json.dumps(ftp_schema, indent=4))

    @staticmethod
    def read_source(
        server: str,
        port: int,
        username_env_name: str,
        password_env_name: str,
        path: str,
        **kwargs: Any,
    ) -> Any:
        """Ftp source reader.

        Args:
            server (str): Server address.
            port (int): Port of the server.
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.
            path (str): Path of the file in the server.

        Returns:
            Any: Data from source.
        """
        user = os.environ.get(username_env_name, "")
        passwd = os.environ.get(password_env_name, "")

        if "file_type" not in kwargs:
            kwargs["file_type"] = find_type(path)

        path = f"ftp://{user}:{passwd}@{server}:{port}/{path}"
        with closing(urllib.request.urlopen(path)) as ftp_file:
            data = super(FtpSource, FtpSource).encode_files(ftp_file, **kwargs)
        return data

    def read(self, source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        args = self.setup_fileinfo(source_info, **kwargs)

        ftp_server = source_info["server"]
        ftp_port = source_info["port"]
        ftp_username = source_info["username_env_name"]
        ftp_password = source_info["password_env_name"]
        ftp_path = source_info["path"]

        data = self.read_source(
            ftp_server, ftp_port, ftp_username, ftp_password, ftp_path, **args
        )

        self.logger.info("Read data from '%s'.", source_info["server"])

        return data
