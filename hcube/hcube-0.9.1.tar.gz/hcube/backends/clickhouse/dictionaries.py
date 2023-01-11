import abc
import hashlib
import json
from dataclasses import dataclass
from typing import Optional


class DataSource(abc.ABC):
    """
    Generic data source for connecting extrenal data sources to clickhouse.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def definition_sql(self):
        """
        Returns the SQL definition of the data source.
        """


class PostgresqlSource(DataSource):
    def __init__(
        self,
        database,
        table=None,
        query=None,
        host="localhost",
        port=5432,
        user="postgres",
        password="",
        invalidate_query=None,
    ):
        super().__init__()
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.table = table
        self.query = query
        self.invalidate_query = invalidate_query
        if not bool(self.table) ^ bool(self.query):
            raise ValueError("Either table or query must be specified, but not both.")

    def definition_sql(self):
        invalidate_query = ""
        if self.invalidate_query:
            invalidate_query = f"invalidate_query '{self.invalidate_query}'"
        # self.table and self.query are mutually exclusive, which is already enforced in
        # the constructor, so we can rely on the fact that only one of them is set.
        table_part = f"table '{self.table}'" if self.table else f"query '{self.query}'"
        return f"""SOURCE(POSTGRESQL(
            port {self.port}
            host '{self.host}'
            user '{self.user}'
            password '{self.password}'
            db '{self.database}'
            {table_part}
            {invalidate_query}
        ))"""


class ClickhouseSource(DataSource):
    def __init__(self, database, table, host="localhost", port=9000, user="default", password=""):
        super().__init__()
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.table = table

    def definition_sql(self):
        return f"""SOURCE(CLICKHOUSE(
            port {self.port}
            host '{self.host}'
            user '{self.user}'
            password '{self.password}'
            db '{self.database}'
            table '{self.table}'
        ))"""


@dataclass
class DictionaryAttr:
    name: str
    type: str
    expression: Optional[str] = None
    null_value: str = "NULL"
    injective: bool = False

    def definition_sql(self):
        expression = f"EXPRESSION {self.expression}" if self.expression else ""
        default = f"DEFAULT {self.null_value}" if self.null_value else ""
        return (
            f"{self.name} {self.type} {default} {expression} "
            f"{'INJECTIVE' if self.injective else ''}"
        )


class DictionaryDefinition:
    def __init__(
        self,
        name: str,
        source: DataSource,
        key: str,
        layout: str,
        attrs: [DictionaryAttr],
        lifetime_min: int = 600,
        lifetime_max: int = 720,
    ):
        self.name = name
        self.key = key
        self.source = source
        self.layout = layout
        self.attrs = attrs
        self.lifetime_min = lifetime_min
        self.lifetime_max = lifetime_max

    def definition_sql(self, database=None):
        db_part = f"{database}." if database else ""
        attrs = ",\n".join([attr.definition_sql() for attr in self.attrs])
        return (
            f"CREATE DICTIONARY {db_part}{self.name} ("
            f"{self.key} UInt64,\n"
            f"{attrs}"
            f") "
            f"PRIMARY KEY {self.key} "
            f"{self.source.definition_sql()} "
            f"LAYOUT ({self.layout.upper()}()) "
            f"LIFETIME(MIN {self.lifetime_min} MAX {self.lifetime_max}) "
            f"COMMENT 'blake2:{self.checksum}'"
        )

    @property
    def checksum(self):
        data = {
            "name": self.name,
            "key": self.key,
            "source": self.source.definition_sql(),
            "layout": self.layout,
            "attrs": [attr.definition_sql() for attr in self.attrs],
            "lifetime_min": self.lifetime_min,
            "lifetime_max": self.lifetime_max,
        }
        return hashlib.blake2b(json.dumps(data).encode("utf-8"), digest_size=32).hexdigest()

    def drop_sql(self, database=None):
        db_part = f"{database}." if database else ""
        return f"DROP DICTIONARY IF EXISTS {db_part}{self.name} SYNC"
