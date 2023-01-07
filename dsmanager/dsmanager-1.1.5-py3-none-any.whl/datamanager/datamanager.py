"""@Author: Rayane AMROUCHE

Datamanager Class.
"""

import os
import json

from typing import Any
from dotenv import load_dotenv  # type: ignore

from dsmanager.datamanager.utils import Utils, DataManagerIOException
from dsmanager.controller.logger import make_logger
from dsmanager.controller.utils import json_to_dict, format_dict
from dsmanager.datamanager.datastorage import DataStorage

from dsmanager.datamanager.datasources.filesource import FileSource
from dsmanager.datamanager.datasources.httpsource import HttpSource
from dsmanager.datamanager.datasources.sqlsource import SqlSource
from dsmanager.datamanager.datasources.ftpsource import FtpSource
from dsmanager.datamanager.datasources.sshsource import SshSource

SOURCES = {
    "file": FileSource,
    "http": HttpSource,
    "sql": SqlSource,
    "ftp": FtpSource,
    "ssh": SshSource,
}

try:
    from dsmanager.datamanager.datasources.sharepointsource import SharepointSource

    SOURCES["sharepoint"] = SharepointSource
except ModuleNotFoundError as m_error:
    print("'SharepointSource' is not available because '{m_error.name}' is missing.")
try:
    from dsmanager.datamanager.datasources.sfsource import SFSource

    SOURCES["salesforce"] = SFSource
except ModuleNotFoundError as m_error:
    print("'SFSource' is not available because '{m_error.name}' is missing.")
try:
    from dsmanager.datamanager.datasources.kagglesource import KaggleSource

    SOURCES["kaggle"] = KaggleSource
except ModuleNotFoundError as m_error:
    print("'KaggleSource' is not available because '{m_error.name}' is missing.")
except (OSError, ValueError) as o_error:
    print("'KaggleSource' is not available.\n" f"More details: {o_error}")


class DataManager:
    """DataManager class handle all the data work."""

    def __init__(
        self,
        metafile_path: str = "data/metadata.json",
        logger_path: str = "/tmp/logs",
        env_path: str | None = None,
        verbose: int = 0,
    ) -> None:
        """Init Datamanager by giving the datasets metadata path.

        Args:
            metafile_path (str, optional): Path of the metadata file of the datasets.
                Defaults to "data/metadata.json".
            logger_path (str, optional): Path of the logger for the DataManager.
                Defaults to "/tmp/logs".
            env_path (str, optional): Path of the env file to be loaded. Defaults to
                None.
            verbose (int, optional): Verbose level for the logger (1 = Log in stdin).
                Defaults to 0.
        """
        if env_path:
            load_dotenv(env_path)
        if metafile_path:
            json_to_dict(metafile_path)

        self.sessions = DataStorage()
        self.datas = DataStorage()
        self.logger = make_logger(
            os.path.join(logger_path, "datamanager"), "datamanager", verbose=verbose
        )
        self.__metadata_path = metafile_path
        self.datasources = DataStorage()
        self.utils = Utils(self, logger_path, verbose)

        for source_name, source_module in SOURCES.items():
            self.add_datasource(source_name, source_module)

    def __repr__(self) -> str:
        res = "DataManager:\n"
        res += f"Metadata's path: {repr(self.__metadata_path)}\n"
        res += f"Metadata: {list(json_to_dict(self.__metadata_path).keys())}\n"
        res += f"Handled sources: {list(self.datasources.keys())}\n"
        res += f"Loaded datas: {list(self.datas.keys())}\n"
        res += f"Loaded sessions: {list(self.sessions.keys())}\n"
        return res

    @classmethod
    def preload(
        cls,
        metafile_path: str = "data/metadata.json",
        logger_path: str = "/tmp/logs",
        env_path: str | None = None,
        verbose: int = 0,
    ) -> Any:
        """Init a DataManager and preload all sources.

        Args:
            metafile_path (str, optional): Path of the metadata file of the datasets.
                Defaults to "data/metadata.json".
            logger_path (str, optional): Path of the logger for the DataManager.
                Defaults to "/tmp/logs".
            env_path (str, optional): Path of the env file to be loaded. Defaults to
                None.
            verbose (int, optional): Verbose level for the logger (1 = Log in stdin).
                Defaults to 0.

        Returns:
            Datamanager: DataManager preloaded.
        """
        self = DataManager(metafile_path, logger_path, env_path, verbose)
        metadata = json_to_dict(self.__metadata_path)
        for key in metadata.keys():
            try:
                self.get_data(key)
                self.logger.info("Preloaded %s.", key)
            except DataManagerIOException as dm_e:
                self.logger.info(
                    "Failed to preload '%s' with message : '%s'.", key, dm_e
                )
        return self

    def add_datasource(self, name: str, source: Any) -> None:
        """Add a source class to datasources dict.

        Args:
            name (str): Name of the source.
            source (DataSource): Data Source class.
        """
        self.datasources[name] = source
        try:
            setattr(self, f"read_{name}", source.read_source)
        except AttributeError as _:
            ...

    def add_source(self, name: str, source_info: dict) -> None:
        """Add a source class to sources dict.

        Args:
            name (str): Name of the source.
            source (DataSource): Data Source class.
        """
        metadata = json_to_dict(self.__metadata_path)
        metadata[name] = source_info
        with open(self.__metadata_path, "w", encoding="utf-8") as metadata_file:
            json.dump(metadata, metadata_file)

    def get_sources(self) -> dict:
        """Getter for metadatas source.

        Returns:
            dict: Metadatas dict.
        """
        metadata = json_to_dict(self.__metadata_path)
        return metadata

    def _get_source_info(self, name: str) -> dict:
        """Handle access to metadata info for a given source.

        Args:
            name (str): Name of the source to access.

        Raises:
            DataManagerIOException: Raised if the name given is not in the metadata.

        Returns:
            dict: Return the metadata of the data source.
        """
        metadata = json_to_dict(self.__metadata_path)
        if name not in metadata:
            raise DataManagerIOException({}, f"{name} not in the metadata file.")
        data = metadata[name]
        return data

    def _get_source_reader(self, source_info: dict) -> Any:
        """Get data sources reader for a given data source's metadata.

        Args:
            source_info (dict): Metadata of a data source.

        Raises:
            DataManagerIOException: Raised if the source is not handled.

        Returns:
            DataSource: Data source reader.
        """
        if "source_type" in source_info:
            source_type = source_info["source_type"]
            del source_info["source_type"]
        else:
            source_type = "file"

        if source_type in self.datasources:
            source_class = self.datasources[source_type]
        else:
            raise DataManagerIOException(source_info)

        return source_class

    def get_data(
        self,
        name: str,
        save: bool = True,
        reload: bool = False,
        formatting: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        """Get info for a given source and return its data.

        Args:
            name (str): Name of the data source.
            save (bool, optional): If True save the data. Defaults to True.
            reload (bool, optional): If False try to load from datas. Defaults to False.
            formatting (dict, optional): Source metadata formatting.

        Returns:
            Any: Requested data.
        """
        if not reload and name in self.datas:
            data = self.datas[name]
        else:
            source_info = self._get_source_info(name)
            if formatting is not None:
                format_dict(source_info, formatting)
            source = self._get_source_reader(source_info)
            data = source(self.logger).read(source_info, **kwargs)
        if save:
            self.datas[name] = data

        return data

    def get_session(
        self,
        name: str,
        save: bool = True,
        reload: bool = False,
        formatting: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        """Get info for a given source and return its data.

        Args:
            name (str): Name of the data source.
            save (bool, optional): If True save the session. Defaults to True.
            reload (bool, optional): If False try to load from sessions. Defaults to
                False.
            formatting (dict, optional): Source metadata formatting.

        Returns:
            Any: Requested session engine.
        """
        if not reload and name in self.sessions:
            data = self.sessions[name]
        else:
            source_info = self._get_source_info(name)
            if formatting:
                format_dict(source_info, formatting)
            source = self._get_source_reader(source_info)
            data = source(self.logger).read_db(source_info, **kwargs)
        if save:
            self.sessions[name] = data

        return data
