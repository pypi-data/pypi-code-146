from dataclasses import (
    dataclass,
)
from deprecated import (
    deprecated,
)
from fa_purity import (
    PureIter,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
    FrozenList,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from redshift_client.column import (
    Column,
    ColumnId,
    ColumnObj,
)
from redshift_client.data_type.core import (
    DataType,
    PrecisionType,
    StaticTypes,
)
from redshift_client.id_objs import (
    TableId,
)
from redshift_client.sql_client import (
    QueryValues,
    RowData,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
    new_query,
)
from redshift_client.table._assert import (
    to_column,
)
from redshift_client.table.core import (
    new as new_table,
    Table,
)
from typing import (
    Callable,
    Dict,
    TypeVar,
)

_T = TypeVar("_T")


def _assert_bool(raw: _T) -> bool:
    if isinstance(raw, bool):
        return raw
    raise TypeError("Expected bool")


@dataclass(frozen=True)
class ManifestId:
    uri: str


def _encode_data_type(d_type: DataType) -> str:
    if isinstance(d_type.value, StaticTypes):
        return d_type.value.value
    if isinstance(d_type.value, PrecisionType):
        return f"{d_type.value.data_type.value}({d_type.value.precision})"
    return f"DECIMAL({d_type.value.precision},{d_type.value.scale})"


@dataclass(frozen=True)
class TableClient:
    _db_client: SqlClient

    def unload(
        self, table: TableId, prefix: str, role: str
    ) -> Cmd[ManifestId]:
        """
        prefix: a s3 uri prefix
        role: an aws role id-arn
        """
        stm = """
            UNLOAD ('SELECT * FROM {schema}.{table}')
            TO %(prefix)s iam_role %(role)s MANIFEST ESCAPE
        """
        args: Dict[str, PrimitiveVal] = {"prefix": prefix, "role": role}
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict({"schema": table.schema.name, "table": table.name}),
            ),
            QueryValues(FrozenDict(args)),
        ).map(lambda _: ManifestId(f"{prefix}manifest"))

    def load(
        self,
        table: TableId,
        manifest: ManifestId,
        role: str,
        nan_handler: bool = True,
    ) -> Cmd[None]:
        """
        If `nan_handler` is disabled, ensure that the table does not contain NaN values on float columns
        """
        nan_fix = "NULL AS 'nan'" if nan_handler else ""
        stm = f"""
            COPY {{schema}}.{{table}} FROM %(manifest_file)s
            iam_role %(role)s MANIFEST ESCAPE {nan_fix}
        """
        args: Dict[str, PrimitiveVal] = {
            "manifest_file": manifest.uri,
            "role": role,
        }
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict({"schema": table.schema.name, "table": table.name}),
            ),
            QueryValues(FrozenDict(args)),
        )

    def get(self, table: TableId) -> Cmd[Table]:
        stm = """
            SELECT ordinal_position,
                column_name,
                data_type,
                CASE WHEN character_maximum_length IS not null
                        THEN character_maximum_length
                        ELSE numeric_precision end AS max_length,
                numeric_scale,
                is_nullable,
                column_default AS default_value
            FROM information_schema.columns
            WHERE table_name = %(table_name)s
                AND table_schema = %(table_schema)s
            ORDER BY ordinal_position
        """
        args: Dict[str, PrimitiveVal] = {
            "table_schema": table.schema.name,
            "table_name": table.name,
        }
        exe = self._db_client.execute(
            new_query(stm),
            QueryValues(FrozenDict(args)),
        )
        results = self._db_client.fetch_all()

        def _extract(raw: FrozenList[RowData]) -> Table:
            columns_pairs = tuple(to_column(column.data) for column in raw)
            columns = FrozenDict(dict(columns_pairs))
            order = tuple(i for i, _ in columns_pairs)
            return new_table(order, columns, frozenset()).unwrap()

        return (exe + results).map(_extract)

    def exist(self, table_id: TableId) -> Cmd[bool]:
        stm = """
            SELECT EXISTS (
                SELECT * FROM information_schema.tables
                WHERE table_schema = %(table_schema)s
                AND table_name = %(table_name)s
            );
        """
        args: Dict[str, PrimitiveVal] = {
            "table_schema": table_id.schema.name,
            "table_name": table_id.name,
        }
        return self._db_client.execute(
            new_query(stm), QueryValues(FrozenDict(args))
        ) + self._db_client.fetch_one().map(
            lambda m: m.map(lambda i: _assert_bool(i.data[0]))
            .to_result()
            .alt(lambda _: TypeError("Expected not None"))
            .unwrap()
        )

    def insert(
        self,
        table_id: TableId,
        table: Table,
        items: PureIter[RowData],
        limit: int,
    ) -> Cmd[None]:
        _fields = ",".join(f"{{field_{i}}}" for i, _ in enumerate(table.order))
        stm = f"""
            INSERT INTO {{schema}}.{{table}} ({_fields}) VALUES %s
        """
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name,
            "table": table_id.name,
        }
        for i, c in enumerate(table.order):
            identifiers[f"field_{i}"] = c.name
        return self._db_client.values(
            dynamic_query(stm, FrozenDict(identifiers)), items, limit
        )

    def rename(self, table_id: TableId, new_name: str) -> Cmd[TableId]:
        stm = """
            ALTER TABLE {schema}.{table} RENAME TO {new_name}
        """
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name,
            "table": table_id.name,
            "new_name": new_name,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        ).map(lambda _: TableId(table_id.schema, new_name))

    def _delete(self, table_id: TableId, cascade: bool) -> Cmd[None]:
        _cascade = "CASCADE" if cascade else ""
        stm = f"""
            DROP TABLE {{schema}}.{{table}} {_cascade}
        """
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name,
            "table": table_id.name,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        )

    def delete(self, table_id: TableId) -> Cmd[None]:
        return self._delete(table_id, False)

    def delete_cascade(self, table_id: TableId) -> Cmd[None]:
        return self._delete(table_id, True)

    def add_column(self, table_id: TableId, column: ColumnObj) -> Cmd[None]:
        stm = f"""
            ALTER TABLE {{table_schema}}.{{table_name}}
            ADD COLUMN {{column_name}}
            {_encode_data_type(column.column.data_type)} DEFAULT %(default_val)s
        """
        identifiers: Dict[str, str] = {
            "table_schema": table_id.schema.name,
            "table_name": table_id.name,
            "column_name": column.id_obj.name,
        }
        args: Dict[str, PrimitiveVal] = {
            "default_val": column.column.default,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)),
            QueryValues(FrozenDict(args)),
        )

    def add_columns(
        self,
        table: TableId,
        columns: FrozenDict[ColumnId, Column],
    ) -> Cmd[None]:
        return (
            from_flist(tuple(columns.items()))
            .map(lambda c: ColumnObj(c[0], c[1]))
            .map(lambda c: self.add_column(table, c))
            .transform(lambda x: consume(x))
        )

    def new(
        self, table_id: TableId, table: Table, if_not_exist: bool = False
    ) -> Cmd[None]:
        enum_primary_keys = tuple(enumerate(table.primary_keys))
        enum_columns = tuple(
            enumerate(tuple((i, table.columns[i]) for i in table.order))
        )
        p_fields = ",".join([f"{{pkey_{i}}}" for i, _ in enum_primary_keys])
        pkeys_template = (
            f",PRIMARY KEY({p_fields})" if table.primary_keys else ""
        )
        not_exists = "" if not if_not_exist else "IF NOT EXISTS"
        encode_nullable: Callable[[bool], str] = (
            lambda b: "NULL" if b else "NOT NULL"
        )
        fields_template: str = ",".join(
            [
                f"""
                    {{name_{n}}} {_encode_data_type(c.data_type)}
                    DEFAULT %(default_{n})s {encode_nullable(c.nullable)}
                """
                for n, (_, c) in enum_columns
            ]
        )
        stm = f"CREATE TABLE {not_exists} {{schema}}.{{table}} ({fields_template}{pkeys_template})"
        identifiers: Dict[str, str] = {
            "schema": table_id.schema.name,
            "table": table_id.name,
        }
        for index, cid in enum_primary_keys:
            identifiers[f"pkey_{index}"] = cid.name
        for index, (cid, _) in enum_columns:
            identifiers[f"name_{index}"] = cid.name
        values = FrozenDict(
            {f"default_{index}": c.default for index, (_, c) in enum_columns}
        )
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), QueryValues(values)
        )

    def create_like(self, blueprint: TableId, new_table: TableId) -> Cmd[None]:
        stm = """
            CREATE TABLE {new_schema}.{new_table} (
                LIKE {blueprint_schema}.{blueprint_table}
            )
        """
        identifiers: Dict[str, str] = {
            "new_schema": new_table.schema.name,
            "new_table": new_table.name,
            "blueprint_schema": blueprint.schema.name,
            "blueprint_table": blueprint.name,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        )

    def move_data(self, source: TableId, target: TableId) -> Cmd[None]:
        """
        This method moves data from source to target.
        After the operation source will be empty.
        Both tables must exists.
        """
        stm = """
            ALTER TABLE {target_schema}.{target_table}
            APPEND FROM {source_schema}.{source_table}
        """
        identifiers: Dict[str, str] = {
            "source_schema": source.schema.name,
            "source_table": source.name,
            "target_schema": target.schema.name,
            "target_table": target.name,
        }
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict(identifiers)), None
        )

    @deprecated(reason="Renamed method, use 'move_data' instead")  # type: ignore[misc]
    def append(self, source: TableId, target: TableId) -> Cmd[None]:
        return self.move_data(source, target)

    def move(self, source: TableId, target: TableId) -> Cmd[None]:
        """
        - create target if not exist
        - move_data (append) data from source into target
        - delete source table
        """
        nothing = Cmd.from_cmd(lambda: None)
        create = self.exist(target).bind(
            lambda b: self.create_like(source, target) if not b else nothing
        )
        return (
            create
            + self.move_data(source, target)
            + self.delete_cascade(source)
        )

    def migrate(self, source: TableId, target: TableId) -> Cmd[None]:
        """
        - delete target if exist
        - move source into target (see move method)
        """
        nothing = Cmd.from_cmd(lambda: None)
        delete = self.exist(target).bind(
            lambda b: self.delete_cascade(target) if b else nothing
        )
        return delete + self.move(source, target)

    @deprecated(reason="Renamed method, use 'migrate' instead")  # type: ignore[misc]
    def overwrite(self, source: TableId, target: TableId) -> Cmd[None]:
        return self.migrate(source, target)
