"""@Author: Rayane AMROUCHE

Sharepoint Sources Handling.
"""

import os
import io
import json

from typing import Any

from shareplum import Site  # type: ignore # pylint: disable=import-error
from shareplum import Office365  # type: ignore # pylint: disable=import-error
from shareplum.site import Version  # type: ignore # pylint: disable=import-error

from dsmanager.datamanager.datasources.datasource import DataSource


class SharepointSource(DataSource):
    """Inherited Data Source Class for sharepoint sources."""

    @staticmethod
    def show_schema() -> None:
        """Get source metadata schema."""
        sharepoint_schema = {
            "source_type": "sharepoint",
            "username_env_name": "onedrive_username_environment_variable_name",
            "password_env_name": "onedrive_password_environment_variable_name",
            "path": "https://sharepoint_address.sharepoint.com/sites/site_name/"
            "folder/file.xlsx",
        }
        sharepoint_schema.update(DataSource.file_schema())
        print(json.dumps(sharepoint_schema, indent=4))

    @staticmethod
    def read_source(
        path: str, username_env_name: str, password_env_name: str, **kwargs: Any
    ) -> Any:
        """Sharepoint source reader.

        Args:
            path (str): Url of the datasource.
            username_env_name (str): Name of the username env variable.
            password_env_name (str): Name of the password env variable.

        Returns:
            Any: Data from source.
        """
        path_split = path.split("/")
        authcookie = Office365(
            "/".join(path_split[:3]),
            username=os.environ.get(username_env_name),
            password=os.environ.get(password_env_name),
        ).GetCookies()
        site = Site(
            "/".join(path_split[:5]),
            version=Version.v365,
            authcookie=authcookie,
        )
        folder = site.Folder("/".join(path_split[5:-1]))
        file = folder.get_file(path_split[-1])

        if isinstance(file, bytes) and "encoding" in kwargs:
            try:
                file = io.StringIO(file.decode(kwargs["encoding"]))
            except UnicodeDecodeError:
                return file

        data = super(SharepointSource, SharepointSource).encode_files(file, **kwargs)
        return data

    def read(self, source_info: dict, **kwargs: Any) -> Any:
        """Handle source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Returns:
            Any: Source datas.
        """
        args = self.setup_fileinfo(source_info, **kwargs)
        sharepoint_path = source_info["path"]
        data = self.read_source(
            sharepoint_path,
            source_info["username_env_name"],
            source_info["password_env_name"],
            **args
        )

        self.logger.info("Read data from '%s'.", sharepoint_path)
        return data
