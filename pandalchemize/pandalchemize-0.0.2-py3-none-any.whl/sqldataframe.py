from __future__ import annotations
from typing import Any, Generator, Mapping, Optional, Sequence

import pandas as pd
import tabulize
from sqlalchemy.engine import Engine

Record = dict[str, Any]


class SqlDataFrame(pd.DataFrame):

    _metadata = ['sqltable', 'primary_keys']

    def __init__(
        self,
        data=None,
        table_name: Optional[str] = None,
        engine: Optional[Engine] = None,
        sqltable: Optional[tabulize.SqlTable] = None,
        *args, 
        **kwargs
    ) -> None:
        super().__init__(data, *args, **kwargs)
        if sqltable is not None:
            self.sqltable = sqltable
            self.table_name = sqltable.table_name
        elif engine is not None and table_name is not None:
            self.sqltable = tabulize.SqlTable(table_name, engine)
            self.table_name = self.sqltable.table_name
            data = self.sqltable.old_records
            super().__init__(data, *args, **kwargs)

    def _sql_constructor(
        self,
        table_name: str,
        engine: Engine
    ) -> SqlDataFrame:
        return SqlDataFrame(
            data=None, table_name=table_name, engine=engine
        ) # type: ignore 

    def _data_constructor(
        self,
        data,
        *args, 
        **kwargs
    ) -> SqlDataFrame:
        return SqlDataFrame(
            data, *args, table_name=self.sqltable.table_name, engine=None,
            sqltable=self.sqltable,  
            **kwargs
        ) # type: ignore 

    @property
    def _constructor(self, *args, **kwargs):
        # used by pandas when it returns a new DataFrame
        return self._data_constructor

    @property
    def primary_keys(self) -> list[str]:
        return self.sqltable.primary_keys

    @primary_keys.setter
    def primary_keys(self, column_names: Sequence[str]) -> None:
        self.sqltable.primary_keys = list(column_names)

    def record_changes(self) -> dict[str, list[Record]]:
        return self.sqltable.record_changes(self)

    def insert_record(self, record: Record) -> None:
        self.loc[len(self.index)] = record

    def insert_records(self, records: Sequence[Record]) -> None:
        for record in records:
            self.insert_record(record)

    def pull(self):
        self.sqltable.pull()

    def push(self) -> None:
        self.sqltable.push(self)
        self.pull()

    def iterrows(self) -> Generator[tuple[int, dict], None, None]:
        for i, (_, series) in enumerate(pd.DataFrame.iterrows(self)):
            yield i, series.to_dict()


class SqlSeries(pd.Series):
    ...

def read_sql(table_name: str, engine: Engine) -> SqlDataFrame:
    return SqlDataFrame(table_name=table_name, engine=engine)

    