import inspect
import os
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional, List

from rick_db.conn import Connection
from rick_db.sql.dialect import PgSqlDialect
from rick_db.util.pg import PgInfo

from pokie.codegen.pg import PgTableSpec, RecordGenerator, RequestGenerator
from pokie.constants import DI_DB, DI_APP
from pokie.core import CliCommand


class CodeGenCommand(CliCommand):
    def get_db(self) -> Optional[Connection]:
        result = None
        di = self.get_di()
        if di.has(DI_DB):
            result = di.get(DI_DB)
        return result

    def is_supported(self, db) -> bool:
        if isinstance(db, Connection):
            return isinstance(db.dialect(), PgSqlDialect)
        return False

    def parse_table_list(self, mgr: PgInfo, table_expr) -> [List, str]:
        schema = mgr.SCHEMA_DEFAULT
        table_list = []
        table_expr = table_expr.split(".", 1)
        table = table_expr[0]
        if len(table_expr) > 1:
            schema = table_expr[0]
            table = table_expr[1]

        all_tables = []
        for tbl in mgr.list_database_tables(schema):
            all_tables.append(tbl.name)

        if table == "*":
            table_list = all_tables
        else:
            if table not in all_tables:
                self.tty.error(
                    "table with name '{}' not found in schema '{}'".format(
                        table, schema
                    )
                )
                return []
            table_list.append(table)

        return table_list, schema

    def pg_gen_dto(self, db, table_expr, dest_file, camel_case=False) -> bool:

        pg = PgTableSpec(db)
        table_list, schema = self.parse_table_list(pg.manager(), table_expr)
        if len(table_list) == 0:
            return False

        gen = RecordGenerator()
        first = True
        result = []
        for name in table_list:
            self.tty.write(
                self.tty.colorizer.white(
                    "generating dto for {}.{}...".format(schema, name), attr="bold"
                )
            )
            spec = pg.table_spec(name, schema)
            result.append(gen.gen_source(spec, camelcase=camel_case, imports=first))
            first = False

        if dest_file is None:
            self.tty.write("\n".join(result))
        else:
            self.tty.write(
                self.tty.colorizer.white("writing to file '{}'...".format(dest_file))
            )
            with open(dest_file, "w") as f:
                f.write("\n".join(result))

            self.tty.write(self.tty.colorizer.green("success!"))
        return True

    def pg_gen_request(
        self, db, table_expr, dest_file, camelcase_id=False, camelcase_cols=False
    ) -> bool:

        pg = PgTableSpec(db)
        table_list, schema = self.parse_table_list(pg.manager(), table_expr)
        if len(table_list) == 0:
            return False

        gen = RequestGenerator()
        first = True
        result = []
        for name in table_list:
            self.tty.write(
                self.tty.colorizer.white(
                    "generating RequestRecord class for {}.{}...".format(schema, name),
                    attr="bold",
                )
            )
            spec = pg.table_spec(name, schema)
            result.append(
                gen.gen_source(
                    spec,
                    camelcase=camelcase_id,
                    db_camelcase=camelcase_cols,
                    imports=first,
                )
            )
            first = False

        if dest_file is None:
            self.tty.write("\n".join(result))
        else:
            self.tty.write(
                self.tty.colorizer.white("writing to file '{}'...".format(dest_file))
            )
            with open(dest_file, "w") as f:
                f.write("\n".join(result))

            self.tty.write(self.tty.colorizer.green("success!"))
        return True


class GenDtoCmd(CodeGenCommand):
    description = "generate dto class from database table"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "table", type=str, help="source table or view for dto generation"
        )
        parser.add_argument("-f", dest="file", type=str, help="destination file")
        parser.add_argument(
            "-c",
            "--camelcase",
            action="store_true",
            default=False,
            help="camelCase attributes",
        )

    def run(self, args) -> bool:
        db = self.get_db()
        if not self.is_supported(db):
            self.tty.error("database code generation is only supported with PostgreSQL")
            return False

        if args.file is not None:
            dest_file = Path(args.file)
            if dest_file.exists():
                self.tty.error("destination file already exists")
                return False

        return self.pg_gen_dto(db, args.table, args.file, args.camelcase)


class GenRequestRecordCmd(CodeGenCommand):
    description = "generate RequestRecord class from database table"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "table", type=str, help="source table or view for request record generation"
        )
        parser.add_argument("-f", dest="file", type=str, help="destination file")
        parser.add_argument(
            "-c",
            "--camelcase-names",
            action="store_true",
            default=False,
            help="camelCase field names",
        )
        parser.add_argument(
            "-C",
            "--camelcase-cols",
            action="store_true",
            default=False,
            help="camelCase bind columns",
        )

    def run(self, args) -> bool:
        db = self.get_db()
        if not self.is_supported(db):
            self.tty.error("database code generation is only supported with PostgreSQL")
            return False

        if args.file is not None:
            dest_file = Path(args.file)
            if dest_file.exists():
                self.tty.error("destination file already exists")
                return False

        return self.pg_gen_request(
            db, args.table, args.file, args.camelcase_names, args.camelcase_cols
        )
