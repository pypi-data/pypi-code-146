import sqlite3
from typing import Iterable, Union

from . import _exceptions
from . import _Table
from . import _internal
from . import _FieldConstraints as _Constr


class DBase:
    """
    SQLite3 database class.
    """
    def __init__(self, dbfile: str):
        self._db_file = dbfile

        self._db_connection = sqlite3.connect(self._db_file)
        self._db_cursor = self._db_connection.cursor()

        self._db_tables = self.get_tables()
        self._active_tables: dict[str, '_Table.Table'] = dict()

    def table(self, table_name: str) -> '_Table.Table':
        """
        Get Table from base.

        Get interactable Table object from this DBase that represents table from base.

        If table with given name have already been initialized with Table object, reference to if will be returned, not new Table object.

        :param table_name: Name of existing table in sqlite3 database.
        :return: new Table object or reference to existing Table object.
        """
        if self.has_table(table_name):
            if table_name in self._active_tables:
                table = self._active_tables[table_name]
            else:
                table = _Table.Table(table_name, self)
                self._active_tables[table_name] = table
            return table
        else:
            raise _exceptions.TableNotFound(table_name, self.name)

    def new_table(self, table_name: str, fields: dict) -> '_Table.Table':
        """
        Create new table in database and get reference Table object for it.

        If table already exists in database, exception will be thrown.

        :param table_name: new table name.
        :param fields: schema for new table.
        :return: new Table object that represents newly created table.
        """
        if self.has_table(table_name):
            raise _exceptions.TableAlreadyExists(table_name, self.name)
        else:
            fields = f'{", ".join(f"{k} {v}" for k, v in fields.items())}'
            query = f'CREATE TABLE {table_name}({fields});'
            self.query(query)
            self._db_connection.commit()

            self._db_tables = self.get_tables()

            return self.table(table_name)

    def query(self, query: str, commit=False):
        """
        Make string SQL query to database.

        :param query: SQL query string.
        :param commit: Either commit changes to database with this query or not.
        :return: query result whatever is is.
        """
        res = self._db_cursor.execute(query)
        if commit:
            self._db_connection.commit()
        return res

    def select(self, source: str, fields: Iterable[str]) -> list[tuple]:
        """
        Select fields from table with no confines.

        :param source: source string name as it is in database.
        :param fields: iterable collection of field string names.
        :return: list of tuples with selected values
        """
        return self.query(f'SELECT {",".join(fields)} FROM {source};').fetchall()

    def insert(self, target_table: str, target_fields: Iterable[str], values: Iterable) -> None:
        """
        Insert values into target table.

        :param target_table: target table string name as it is in database.
        :param target_fields: iterable collection of target fields
        :param values: iterable collection of target values
        :return:
        """
        f_names = []
        f_values = []
        for f, v in zip(target_fields, _internal.proper_values(values)):
            if v == "NULL":
                continue
            f_names.append(f)
            f_values.append(v)

        self.query(f'INSERT INTO {target_table}({",".join(f_names)}) VALUES({",".join(f_values)});', commit=True)
        self._db_connection.commit()

    def drop(self, target_table: str, suppress_nonexisting=False) -> None:
        """
        Drop table from current DBase.

        :param target_table: target table name as it is in sqlite base
        :param suppress_nonexisting: True -- add 'IF EXISTS', so no error on table is not in db
        """
        self.query(f'DROP TABLE {target_table} {"IF EXISTS" if suppress_nonexisting else ""};')

    def has_tables(self, tables: Iterable[Union[str, '_Table.Table']]) -> bool:
        """
        Check if all given tables are present in database.

        :param tables: iterable collection of string table names or of Table objects to check
        :return: True if all tables are present
        """
        for table in tables:
            if not self.has_table(table):
                return False
        return True

    def has_table(self, table_name: Union[str,'_Table.Table']) -> bool:
        """
        Check if given table is present in database.

        :param table_name: string name of table of Table object to check
        :return: True if table is present
        """
        table_name = table_name if isinstance(table_name, str) else table_name.name
        return table_name in self._db_tables

    def get_tables(self) -> set[str]:
        """
        Get all tables from database with SQL query.

        :return: set of table names
        """
        tables = self.query('SELECT name from sqlite_master where type="table"').fetchall()
        return set(t[0] for t in tables)

    def get_fields(self, table: str) -> dict[str, '_Table.TableField']:
        """
        Get fields for of given table.

        If table is not present, exception will be thrown.

        Also, when call this method, table will be registered in DBase and Table object for given table will be created.

        :param table: string name of table as it is in database.
        :return: dict of {field_name: TableField object}
        """
        if not self.has_table(table):
            raise _exceptions.TableNotFound(table, self.name)

        table = self.table(table)
        return self.table_fields(table)

    def get_foreign_keys(self, table: str) -> dict[str, '_Table.TableFK']:
        """
        Get foreign keys of given table.

        If table is not present, exception will be thrown.

        Also, when call this method, table will be registered in DBase and Table object for given table will be created.

        :param table: table string name as it is in base.
        :return: dict of {field_name: TableFK}
        """
        if not self.has_table(table):
            raise _exceptions.TableNotFound(table, self.name)

        table = self.table(table)
        return self.table_foreign_keys(table)

    def table_satisfied(self, table: '_Table.Table') -> bool:
        """
        Check if all tables binded to some Table object are present in database.

        Useful for non-real Tables.

        :param table: Table object reference.
        :return: True if all binded tables are present in base.
        """
        return self.has_tables(table.binded)

    def tables_satified(self, tables: Iterable['_Table.Table']) -> bool:
        """
        Check if all tables binded to all given Table objects are present in database.

        Useful for non-real Tables.

        :param tables: Iterable of Table object references.
        :return: True if all binded tables for all given Table objects are present in base.
        """
        for t in tables:
            return self.table_satisfied(t)
        return True

    def table_fields(self, table: '_Table.Table') -> dict[str, '_Table.TableField']:
        """
        Get fields for of given table.

        :param table: Table reference object.
        :return: dict of {field_name: TableField object}
        """
        result = self.query(f'PRAGMA table_info({table.query})').fetchall()
        fks = self.query(f'PRAGMA foreign_key_list({table.query})').fetchall()
        fields = dict()
        for i, name, typ, nullable, default, pk in result:
            constraints = []
            if pk != 0:
                constraints.append(_Constr.Primary(pk))
            if not nullable:
                constraints.append(_Constr.NotNull())
            if default:
                constraints.append(_Constr.Default(default))
            fields.update({f"{table.name}.{name}": _Table.TableField(i, name, typ, table, constraints=constraints)})

        for fk in fks:
            master_name = fk[2]
            master_field = fk[4]
            slave_field = fk[3]
            fields[f'{table.name}.{slave_field}'].constraints.append(_Constr.Foreign(f'{master_name}.{master_field}'))

        return fields

    def table_foreign_keys(self, table: '_Table.Table') -> dict[str, '_Table.TableFK']:
        """
        Get foreign keys for of given table.

        :param table: Table reference object.
        :return: dict of {field_name: TableFK object}
        """
        result = self.query(f'PRAGMA foreign_key_list({table.query})').fetchall()
        keys = dict()

        for f in result:
            master = self.table(f[2])
            fk = _Table.TableFK(master.field_by_name(f[4]), table.field_by_name(f[3]))
            keys[f'{table.name}.{fk.slave_field.name}'] = fk

        return keys

    @property
    def name(self) -> str:
        """Name of current DBase's file."""
        return self._db_file

    @property
    def tables(self) -> set[str]:
        """All tables present in current DBase's file."""
        return self._db_tables

    @property
    def active_tables(self) -> dict[str, '_Table.Table']:
        """All Table objects initialized within DBase."""
        return self._active_tables.copy()

    def __repr__(self) -> str:
        return f'DBase<{self.name}>'

    def __del__(self):
        self._db_cursor.close()
        self._db_connection.close()
