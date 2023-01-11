from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
)
from fa_purity.json.primitive.factory import (
    to_primitive,
)
from fa_purity.pure_iter.factory import (
    from_flist,
)
from fa_purity.pure_iter.transform import (
    consume,
)
from fa_purity.utils import (
    raise_exception,
)
from redshift_client.id_objs import (
    SchemaId,
    TableId,
)
from redshift_client.schema.core import (
    Quota,
    SchemaPolicy,
)
from redshift_client.sql_client import (
    QueryValues,
    SqlClient,
)
from redshift_client.sql_client.primitive import (
    PrimitiveVal,
)
from redshift_client.sql_client.query import (
    dynamic_query,
    new_query,
)
from redshift_client.table.client import (
    TableClient,
)
from typing import (
    Callable,
    Dict,
    FrozenSet,
    TypeVar,
)

_T = TypeVar("_T")


def _assert_bool(raw: _T) -> bool:
    if isinstance(raw, bool):
        return raw
    raise TypeError("Expected bool")


@dataclass(frozen=True)
class SchemaClient:
    _db_client: SqlClient

    def all_schemas(self) -> Cmd[FrozenSet[SchemaId]]:
        _stm = (
            "SELECT s.nspname AS table_schema",
            "FROM pg_catalog.pg_namespace s",
            "JOIN pg_catalog.pg_user u ON u.usesysid = s.nspowner",
            "ORDER BY table_schema",
        )
        stm = " ".join(_stm)
        return self._db_client.execute(
            new_query(stm), None
        ) + self._db_client.fetch_all().map(
            lambda i: frozenset(
                SchemaId(to_primitive(e.data[0], str).unwrap()) for e in i
            )
        )

    def table_ids(self, schema: SchemaId) -> Cmd[FrozenSet[TableId]]:
        _stm = (
            "SELECT tables.table_name FROM information_schema.tables",
            "WHERE table_schema = %(schema_name)s",
        )
        stm = " ".join(_stm)
        args: Dict[str, PrimitiveVal] = {"schema_name": schema.name}
        return self._db_client.execute(
            new_query(stm), QueryValues(FrozenDict(args))
        ) + self._db_client.fetch_all().map(
            lambda i: frozenset(
                TableId(schema, to_primitive(e.data[0], str).unwrap())
                for e in i
            )
        )

    def exist(self, schema: SchemaId) -> Cmd[bool]:
        _stm = (
            "SELECT EXISTS",
            "(SELECT 1 FROM pg_namespace",
            "WHERE nspname = %(schema_name)s)",
        )
        stm = " ".join(_stm)
        args: Dict[str, PrimitiveVal] = {"schema_name": schema.name}
        return self._db_client.execute(
            new_query(stm), QueryValues(FrozenDict(args))
        ) + self._db_client.fetch_one().map(lambda x: x.value_or(None)).map(
            lambda i: _assert_bool(i.data[0])
            if i is not None
            else raise_exception(TypeError("Expected not None"))
        )

    def _delete(self, schema: SchemaId, cascade: bool) -> Cmd[None]:
        opt = " CASCADE" if cascade else ""
        stm: str = "DROP SCHEMA {schema_name}" + opt
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict({"schema_name": schema.name})), None
        )

    def delete(self, schema: SchemaId) -> Cmd[None]:
        return self._delete(schema, False)

    def delete_cascade(self, schema: SchemaId) -> Cmd[None]:
        return self._delete(schema, True)

    def rename(self, old: SchemaId, new: SchemaId) -> Cmd[None]:
        stm = "ALTER SCHEMA {from_schema} RENAME TO {to_schema}"
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict(
                    {
                        "from_schema": old.name,
                        "to_schema": new.name,
                    }
                ),
            ),
            None,
        )

    def create(
        self, schema: SchemaId, if_not_exist: bool = False
    ) -> Cmd[None]:
        not_exist = " IF NOT EXISTS " if if_not_exist else ""
        stm = f"CREATE SCHEMA {not_exist} {{schema}}"
        return self._db_client.execute(
            dynamic_query(stm, FrozenDict({"schema": schema.name})), None
        )

    def _recreate(self, schema: SchemaId, cascade: bool) -> Cmd[None]:
        nothing = Cmd.from_cmd(lambda: None)
        return self.exist(schema).bind(
            lambda b: self._delete(schema, cascade) if b else nothing
        ) + self.create(schema)

    def recreate(self, schema: SchemaId) -> Cmd[None]:
        return self._recreate(schema, False)

    def recreate_cascade(self, schema: SchemaId) -> Cmd[None]:
        return self._recreate(schema, True)

    def _move(
        self,
        source: SchemaId,
        target: SchemaId,
        move_op: Callable[[TableId, TableId], Cmd[None]],
    ) -> Cmd[None]:
        return (
            self.table_ids(source)
            .map(lambda x: from_flist(tuple(x)))
            .bind(
                lambda p: p.map(
                    lambda t: move_op(t, TableId(target, t.name))
                ).transform(lambda x: consume(x))
            )
        ) + self.delete(source)

    def migrate(self, source: SchemaId, target: SchemaId) -> Cmd[None]:
        """
        Moves all tables from `source` to `target` overwriting `target` data.
        Deletes empty source after success.
        """
        _client = TableClient(self._db_client)
        return self._move(source, target, _client.migrate)

    def move(self, source: SchemaId, target: SchemaId) -> Cmd[None]:
        """
        Moves all tables from `source` to `target`.
        It does not overwrite target data.
        Deletes empty source after success.
        """
        _client = TableClient(self._db_client)
        return self._move(source, target, _client.move)

    def set_policy(self, schema: SchemaId, policy: SchemaPolicy) -> Cmd[None]:
        stm = "ALTER SCHEMA {schema} OWNER TO {owner}"
        stm2 = (
            f"ALTER SCHEMA {{schema}} QUOTA %(quota)s {policy.quota.unit.value}"
            if isinstance(policy.quota, Quota)
            else "ALTER SCHEMA {schema} QUOTA UNLIMITED"
        )
        set_owner = self._db_client.execute(
            dynamic_query(
                stm, FrozenDict({"schema": schema.name, "owner": policy.owner})
            ),
            None,
        )
        id_args: Dict[str, str] = {"schema": schema.name}
        args: Dict[str, PrimitiveVal] = (
            {"quota": policy.quota.value}
            if isinstance(policy.quota, Quota)
            else {}
        )
        set_quota = self._db_client.execute(
            dynamic_query(stm2, FrozenDict(id_args)),
            QueryValues(FrozenDict(args)),
        )
        return set_owner + set_quota
