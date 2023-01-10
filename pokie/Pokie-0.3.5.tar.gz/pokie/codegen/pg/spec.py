from typing import Optional

from rick_db.conn import Connection
from rick_db.util.pg.records import ColumnRecord
from rick_db.util.pg import PgInfo

from pokie.codegen.spec import TableSpec, FieldSpec


class PgTableSpec:
    def __init__(self, conn: Connection):
        self.db = conn
        self.mgr = PgInfo(conn)
        self._tables = {}
        self._indexes = {}

    def manager(self):
        return self.mgr

    def get_pk(self, table, schema) -> Optional[str]:
        for f in self.mgr.list_table_indexes(table, schema):
            if f.primary:
                return f.field
        return None

    def get_fields(self, table, schema) -> dict:
        result = {}
        for c in self.mgr.list_table_columns(table, schema):
            result[c.column] = c
        return result

    def is_serial(self, table, field, schema) -> bool:
        namespec = "{}.{}".format(schema, table)
        sql = "SELECT pg_get_serial_sequence(%s, %s)"
        with self.db.cursor() as c:
            return len(c.exec(sql, (namespec, field))) > 0

    def get_fk(self, table, schema) -> dict:
        result = {}
        for r in self.mgr.list_table_foreign_keys(table, schema):
            result[r.column] = r
        return result

    def spec_bpchar(self, f: ColumnRecord) -> dict:
        if f.maxlen is not None:
            return {"maxlen": f.maxlen}
        return {}

    def spec_varchar(self, f: ColumnRecord) -> dict:
        if f.maxlen is not None:
            return {"maxlen": f.maxlen}
        return {}

    def spec_numeric(self, f: ColumnRecord) -> dict:
        return {
            "precision": f.numeric_precision,
            "cardinal": f.numeric_precision_cardinal,
        }

    def table_spec(self, table, schema: str = None) -> TableSpec:
        """
        Generate a table spec for the given table
        :param table:
        :param schema:
        :return: TableSpec object
        """
        if schema is None:
            schema = PgInfo.SCHEMA_DEFAULT

        pk = self.get_pk(table, schema)
        fks = self.get_fk(table, schema)
        fields = self.get_fields(table, schema)
        identity = None
        pk_auto = False

        for name, f in fields.items():
            if f.is_identity == "YES":
                identity = name
                break

        # primary key may not exist as key, but table may have an identity column
        # if we find an always generated identity column, we'll use that
        if pk is None and identity is not None:
            pk = identity
            pk_auto = True

        if pk is not None:
            if pk not in fields.keys():
                raise RuntimeError(
                    "Primary key '{}' does not exist in table field list for table {}.{}".format(
                        pk, schema, table
                    )
                )

            if not pk_auto:
                # pk_auto is true if pk is serial or if pk is an identity column
                pk_auto = self.is_serial(table, pk, schema) or str(pk) == str(identity)

        spec = TableSpec(table=table, schema=schema, pk=pk, fields=[])
        for name, f in fields.items():
            is_pk = pk == f.column
            auto = is_pk and pk_auto

            spec_formatter = getattr(self, "spec_" + f.udt_name, None)
            type_spec = {}
            if callable(spec_formatter):
                type_spec = spec_formatter(f)

            field = FieldSpec(
                name=f.column,
                pk=is_pk,
                auto=auto,
                nullable=f.is_nullable == "YES",
                fk=False,
                fk_table=None,
                fk_schema=None,
                fk_column=None,
                dtype=f.udt_name,
                dtype_spec=type_spec,
            )

            if f.column in fks.keys():
                field.fk = True
                field.fk_table = fks[f.column].foreign_table
                field.fk_schema = fks[f.column].foreign_schema
                field.fk_column = fks[f.column].foreign_column

            spec.fields.append(field)

        return spec
