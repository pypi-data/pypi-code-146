import os
from collections.abc import Mapping
from typing import Dict, Optional, Union

# loaded config
conf = {
    "folders": {
        "data": "data",
        "source": "data/source",
        "processed": "data/processed",
        "public": "data/public",
        "untracked": "data/untracked",
        "output": "output",
        "etl": "etl",
        "eda": "eda",
        "publish": "publish",
        "report": "report",
    },
    "urls": {
        "bord4-data": "https://raw.githubusercontent.com/BergensTidende/bord4-data/",
        "norwegian-population": "https://raw.githubusercontent.com/BergensTidende/bord4-data/master/data/csv/norwegian_population.csv",  # noqa: E501
    },
}


class Config(object):
    """
    This class is used to get the configuration of the project.
    Gives easy access to commonly used paths to folders and urls.
    """

    def __init__(self, module_path: str) -> None:
        self._config = conf  # set it to conf
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.project_root = module_path

    def get_property(self, property_name: str) -> Optional[Union[str, Dict[str, str]]]:
        """Get root property from the config.

        Args:
            property_name (str): the name of the property to get

        Returns:
            Union[str, Dict[str, str]]: the value of the property,
            or a dict of child properties
        """
        if property_name not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]

    def get_folder(self, folder_name: str) -> Optional[str]:
        """ "
        Args:
            folder_name (str): the name of the folder to get

        Returns:
            Optional[str]: the path to the folder, or None if not found
        """
        if folder_name == "root":
            return self.project_root

        folder = self.folders.get(folder_name, None)

        if folder is None:
            return None

        folder_path = os.path.join(self.project_root, folder)
        return folder_path

    def get_url(self, url_name: str) -> Optional[str]:
        """Get a url from the config.

        Args:
            url_name (str): the name of the url to get

        Returns:
            Optional[str]: the url, or None if not found
        """
        return self.urls.get(url_name, None)

    @property
    def folders(self) -> Dict[str, str]:
        """Get the folders property from the config."""
        folders = self.get_property("folders")

        if folders is None:
            return {}

        if not isinstance(folders, Mapping):
            raise TypeError("folders must be a dictionary")

        return folders

    @property
    def urls(self) -> Dict[str, str]:
        """Get the urls property from the config."""
        urls = self.get_property("urls")

        if urls is None:
            return {}

        if not isinstance(urls, Mapping):
            raise TypeError("urls must be a dictionary")

        return urls

    @property
    def root(self) -> str:
        """Get the root property from the config."""
        return self.project_root

    @property
    def processed(self) -> str:
        """Get the processed folder from the config."""
        folder = self.get_folder("processed")

        if folder is None:
            raise ValueError("processed folder not found in config")

        return folder

    @property
    def source(self) -> str:
        """Get the source folder from the config."""
        folder = self.get_folder("source")

        if folder is None:
            raise ValueError("processed folder not found in config")

        return folder

    @property
    def public(self) -> str:
        """Get the public folder from the config."""
        folder = self.get_folder("public")

        if folder is None:
            raise ValueError("processed folder not found in config")

        return folder

    @property
    def output(self) -> str:
        """Get the output folder from the config."""
        folder = self.get_folder("output")

        if folder is None:
            raise ValueError("processed folder not found in config")

        return folder

    def get_file_path(self, folder_name: str, file_name: str) -> str:
        """Get the path to a file in the project root.

        Args:
            folder_name (str): the name of the folder
            file_name (str): the name of the file

        Returns:
            str: the path to the file
        """

        folder = self.get_folder(folder_name)

        if folder is None:
            raise ValueError("folder not found in config")

        return os.path.join(folder, file_name)

    def get_source_file(self, file_name: str) -> str:
        """Get the path to a file in the source folder.

        Args:
            file_name (str): the name of the file

        Returns:
            str: the path to the file
        """
        return self.get_file_path("source", file_name)

    def get_processed_file(self, file_name: str) -> str:
        """Get the path to a file in the processed folder.

        Args:
            file_name (str): the name of the file

        Returns:
            str: the path to the file
        """
        return self.get_file_path("processed", file_name)

    def get_public_file(self, file_name: str) -> str:
        """Get the path to a file in the public folder.

        Args:
            file_name (str): the name of the file

        Returns:
            str: the path to the file
        """
        return self.get_file_path("public", file_name)

    def get_untracked_file(self, file_name: str) -> str:
        """Get the path to a file in the untracked folder.

        Args:
            file_name (str): the name of the file

        Returns:
            str: the path to the file
        """
        return self.get_file_path("untracked", file_name)

    def get_output_file(self, file_name: str) -> str:
        """Get the path to a file in the output folder.

        Args:
            file_name (str): the name of the file

        Returns:
            str: the path to the file
        """
        return self.get_file_path("output", file_name)
