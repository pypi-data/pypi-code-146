"""@Author: Rayane AMROUCHE

Data Sources Handling.
"""

from typing import Any
from logging import Logger

import pandas as pd  # type: ignore

from dsmanager.datamanager.utils import DataManagerIOException


class DataSource:
    """Data Source Class."""

    def __init__(self, logger: Logger) -> None:
        """Init a Data Source.

        Args:
            logger (Logger): Passed down logger from the Data Manager.
        """
        self.logger = logger

    @staticmethod
    def file_schema() -> dict:
        """Get file types schema arguments.

        Returns:
            dict: file types schema arguments.
        """
        return {
            "file_type": "csv | excel | text | json | ...",
            "encoding": "utf-8",
            "args": {"pandas_read_file_argument_keyword": "value_for_this_argument"},
        }

    @staticmethod
    def setup_fileinfo(source_info: dict, **kwargs: Any) -> dict:
        """Update args with source_info if needed.

        Args:
            source_info (dict): Source metadata.
        """
        DataSource.load_source(source_info, **kwargs)
        args = source_info["args"] if "args" in source_info else {}
        if "file_type" in source_info:
            args["file_type"] = source_info["file_type"]
        if "encoding" in source_info:
            args["encoding"] = source_info["encoding"]
        return args

    @staticmethod
    def encode_files(
        file: str, file_type: str = "csv", encoding: str = "utf-8", **kwargs: Any
    ) -> Any:
        """Encode file and read it with the correct method depending on the file type.

        Args:
            file (str): File or path of the file to encode.
            file_type (str, optional): Type of file. efaults to "csv".
            encoding (str, optional): Type of encoding to apply on the file. Defaults to
                "utf-8".

        Raises:
            Exception: Raised if the file type is not handled.

        Returns:
            Any: File encoded.
        """
        data = None
        if file_type == "csv":
            data = pd.read_csv(file, **kwargs)
        elif file_type == "excel":
            data = pd.read_excel(file, **kwargs)
        elif file_type == "json":
            data = pd.Series(file)
        elif file_type == "text":
            with open(file, "r", encoding=encoding) as file_obj:
                data = file_obj.read()
        else:
            raise Exception("File type unknown or not supported.")
        return data

    @staticmethod
    def load_source(source_info: dict, **kwargs: Any) -> None:
        """Update source info with kwargs.

        Args:
            source_info (dict): Source metadata to update.
        """
        if "args" not in source_info:
            source_info["args"] = {}
        source_info["args"].update(**kwargs)

    def read(self, source_info: dict, **kwargs: Any) -> None:
        """Read source and returns the source data.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            DataManagerIOException: Raised if missing needed metadatas.
        """
        DataSource.load_source(source_info, **kwargs)
        raise DataManagerIOException(source_info, "This source does not handle read.")

    def read_db(self, source_info: dict, **kwargs: Any) -> None:
        """Read source and returns a source engine.

        Args:
            source_info (dict): Source metadatas.

        Raises:
            Exception: Raised if missing needed metadatas.
        """
        DataSource.load_source(source_info, **kwargs)
        raise DataManagerIOException(
            source_info, "This source does not handle read_db."
        )
