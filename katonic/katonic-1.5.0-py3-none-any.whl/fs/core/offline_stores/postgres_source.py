#!/usr/bin/env python
#
# Copyright (c) 2022 Katonic Pty Ltd. All rights reserved.
#

from typing import Callable, Dict, Iterable, Optional, Tuple
from katonic.fs.core.offline_stores.postgres_util import get_postgres_conn

from katonic.fs.data_source import DataSource, SourceType
from katonic.fs.repo_config import RepoConfig
from katonic.fs.type_map import pg_type_code_to_pg_type, pg_type_to_kfs_value_type
from katonic.fs.value_type import ValueType


class PostgreSQLSource(DataSource):
    def __init__(
        self,
        query: str,
        event_timestamp_column: Optional[str] = "", # necessary parameter
        created_timestamp_column: Optional[str] = "",
        # table_ref: Optional[str] = None,
        # field_mapping: Optional[Dict[str, str]] = None,
        # date_partition_column: Optional[str] = "",
    ):
        self._postgres_options = PostgreSQLOptions(query=query)

        super().__init__(
            event_timestamp_column,
            created_timestamp_column,
        )

    def __eq__(self, other):
        if not isinstance(other, PostgreSQLSource):
            raise TypeError(
                "Comparisons should only involve BigQuerySource class objects."
            )

        return (
            self._postgres_options.query == other._postgres_options._query
            and self.event_timestamp_column == other.event_timestamp_column
            and self.created_timestamp_column == other.created_timestamp_column
        )

    @staticmethod
    def from_dict(data_source: Dict):
        assert "custom_options" in data_source

        postgres_options = data_source["custom_options"]["configuration"]
        return PostgreSQLSource(
            query=postgres_options["query"],
            event_timestamp_column=data_source["event_timestamp_column"],
            created_timestamp_column=data_source["created_timestamp_column"],
        )

    def to_dict(self) -> Dict:
        return {
            "type": SourceType.BATCH_FILE.name,
            "custom_options": self._postgres_options.to_dict(),
            "event_timestamp_column": self.event_timestamp_column,
            "created_timestamp_column": self.created_timestamp_column,
        }

    def validate(self, config: RepoConfig):
        pass

    @staticmethod
    def source_datatype_to_kfs_value_type() -> Callable[[str], ValueType]:
        return pg_type_to_kfs_value_type

    def get_table_column_names_and_types(
        self, config: RepoConfig
    ) -> Iterable[Tuple[str, str]]:
        with get_postgres_conn(config.offline_store) as conn, conn.cursor() as cur:
            cur.execute(
                f"SELECT * FROM ({self.get_table_query_string()}) AS sub LIMIT 0"
            )
            return (
                (c.name, pg_type_code_to_pg_type(c.type_code)) for c in cur.description
            )
    
    def get_table_query_string(self) -> str:
        return f"({self._postgres_options._query})"
    

class PostgreSQLOptions:
    """
    DataSource PostgreSQL options used to source features from PostgreSQL query
    """
    def __init__(self, query: Optional[str]):
        self._query = query

    @property
    def query(self):
        """
        Returns the BigQuery SQL query referenced by this source
        """
        return self._query

    @query.setter
    def query(self, query):
        """
        Sets the BigQuery SQL query referenced by this source
        """
        self._query = query

    @classmethod
    def from_dict(cls, postgres_options_dict: Dict):
        config = postgres_options_dict["configuration"]
        return cls(query=config["query"],)

    def to_dict(self) -> Dict:
        return {
            "configuration": {"query": self.query},
        }

