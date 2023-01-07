from dataclasses import dataclass
from enum import Enum
import pandas as pd
import requests
from io import BytesIO
from typing import Dict, List, Any, Optional, Tuple
from canner.request import CannerRequest
from canner.logging import *


@dataclass
class ParquetQueryResult(object):
    columns: List[Dict[str, Any]]
    data: Any


class ParquetSourceType(Enum):
    URL = "URL"
    FILE_PATH = "FILE_PATH"


class ParquetReader(object):
    def __init__(
        self,
        source_type: ParquetSourceType,
        sources: List[str],
        engine: str = "fastparquet",
    ) -> None:
        """
        The Args:
        source_type (ParquetSourceType): The read parquet source type
        sources (List[str]): read multi related parquet sources
        engine (str): the engine for parquet to read
        """
        self._source_type = source_type
        self._sources = sources
        self._engine = engine

    def read_to_df(self, limit: Optional[int] = None, offset: int = 0) -> pd.DataFrame:
        """
        Read the parquet source to data frame
        Args:
            limit (Optional[int]): The limit location of the content read
            offset (int): The starter location of the content read, the default = 0
        Returns:
            Dataframe: the read content
        """
        collected_dfs = []
        collected_count = 0
        for source in self._sources:
            df = self._read_from_source(source, self._source_type)
            collected_count += df.shape[0]
            collected_dfs.append(df)
            # if we get enough data, stop getting the next url dataframes
            if not limit is None:
                if collected_count >= int(limit) + offset:
                    break
        # concat collected dataframes from urls
        result: pd.DataFrame = pd.concat(collected_dfs)
        if not limit is None:
            result = result.iloc[offset : limit + offset, :]
        return result

    def read_to_list(
        self, limit: Optional[int] = None, offset: int = 0
    ) -> Tuple[List[Dict[str, Any]], List[Any]]:
        """
        Read the parquet source and convert to list
        Args:
            limit (Optional[int]): The limit location of the content read
            offset (int): The starter location of the content read, the default = 0
        Returns:
            Tuple[List[Dict[str, Any]], List[Any]]: The columns and list converted content
        """
        df = self.read_to_df(limit, offset)
        # transfer format to list data
        return self.convert_to_list(df)

    @staticmethod
    def convert_to_list(df: pd.DataFrame) -> Tuple[List[Dict[str, Any]], List[Any]]:
        """
        Convert data frame to list
        Args:
            df (DataFrame): The DataFrame type data
        Returns:
            Tuple[List[Dict[str, Any]], List[Any]]: The columns and list converted content
        """
        # transfer format to list data
        columns = list(map(lambda column: {"name": column}, list(df.columns)))
        # keep each row be object type to preventing numpy auto convert type
        result = [row.astype("object").to_numpy().tolist() for _, row in df.iterrows()]
        return columns, result

    def _read_from_source(self, source: str, source_type: ParquetSourceType):
        # source_type is url
        if source_type == ParquetSourceType.URL:
            resp = requests.get(source)
            return pd.read_parquet(BytesIO(resp.content), engine=self._engine)
        # source_type is file path
        return pd.read_parquet(source, engine=self._engine)


class ParquetQueryReader(object):
    def __init__(
        self,
        query_id: str,
        workspace_id: str,
        request: CannerRequest,
    ) -> None:

        self._query_id = query_id
        self._workspace_id = workspace_id
        self._request = request
        self._storage_urls = self.__retrieve_storage_urls()

    def read(self, limit: int, offset: int) -> ParquetQueryResult:
        self.__check_nested_collection_and_warning()
        if len(self._storage_urls) == 0:
            data = pd.DataFrame({}).to_numpy().tolist()
            return ParquetQueryResult([], data)

        # The storage urls not empty
        columns, data = ParquetReader(
            ParquetSourceType.URL, self._storage_urls
        ).read_to_list(limit, offset)
        return ParquetQueryResult(columns, data)

    def __retrieve_storage_urls(self) -> List[str]:
        path_url = f"api/v1/query/{self._query_id}/result/signedUrls?workspaceId={self._workspace_id}"
        return self._request.get(path_url).get("signedUrls")

    def __check_nested_collection_and_warning(self):
        result = self._request.get(
            f"api/v1/query/{self._query_id}?workspaceId={self._workspace_id}"
        )
        columns = result["columns"]
        logger = get_logger("Query", log_level=logging.WARNING)
        for column in columns:
            if self.__is_collection(column["typeSignature"]["rawType"]):
                for eleColumn in column["typeSignature"]["arguments"]:
                    if eleColumn["kind"] == "TYPE":
                        if self.__is_collection(eleColumn["value"]["rawType"]):
                            logger.warning(
                                f"Nested Collection isn't supported in fetchBy-storage-mode. Column %s: %s "
                                f"would be None.",
                                column["name"],
                                column["type"],
                            )
                    elif eleColumn["kind"] == "NAMED_TYPE":
                        if self.__is_collection(
                            eleColumn["value"]["typeSignature"]["rawType"]
                        ):
                            logger.warning(
                                f"Nested Collection isn't supported in fetchBy-storage-mode. Column %s: %s "
                                f"would be None.",
                                column["name"],
                                column["type"],
                            )

    def __is_collection(self, type):
        if ["array", "map", "row"].__contains__(type):
            return True
        return False
