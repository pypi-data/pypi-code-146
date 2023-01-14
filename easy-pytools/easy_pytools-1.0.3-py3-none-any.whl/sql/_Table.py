from typing import Iterable, Union, Mapping, Any, Sequence
from . import _Base
from . import _Query
from . import _FieldConstraints as _Constr
from . import aggregate


class Table:
    """
    Table object which represents SQL table or SQL composition of Table objects.
    """
    def __init__(self, table_name: str, db_obj: '_Base.DBase', table_query: str = None, binded_tables: Iterable['Table'] = None):
        self._name = table_name
        self._query = table_name if table_query is None else table_query
        self._is_real = binded_tables is None
        self._db = db_obj
        self._binded = {self} if self.is_real else set()
        if binded_tables is not None:
            for rqt in binded_tables:
                self._binded.update(rqt.binded)

        self._fields = dict()
        self._foreign_keys = dict()
        for rqt in self.binded:
            self._fields.update(db_obj.table_fields(rqt))
            self._foreign_keys.update(db_obj.table_foreign_keys(rqt))

        self._foreign_tables = set()
        for f, fk in self.foreign_keys.items():
            self._foreign_tables.add(fk.master_field.table)

        for field in self.fields.values():
            self.__dict__.update({f'f_{field.name}': field})

    def field_by_name(self, field_name: str) -> 'TableField':
        """
        Get TableField reference by field_name from this Table.

        :param field_name: field name with (or without) real Table name reference.
        :return:
        """
        return self._fields[self.field_from_name(field_name)]

    def field_from_name(self, field_name: str) -> str:
        """
        Copmile <Table_Name>.<Field_Name> from only Field_Name for one of this Table's real binded Tabled.

        If field is not present in Table, raise KeyError.

        :param field_name: field name.
        :return: field name with this Table's name reference
        """
        if "." in field_name:
            return field_name
        for try_table in self.binded:
            if self.has_field(fname := f'{try_table.name}.{field_name}'):
                return fname
        raise KeyError(f"{self} has no field {field_name}")

    def has_field(self, field_name: str) -> bool:
        """
        Is this Table has field.

        :param field_name: field name with (or without) real Table name reference.
        :return: This Table contains field
        """
        if "." in field_name:
            return field_name in self.fields
        else:
            for try_table in self.binded:
                if (fname := f'{try_table.name}.{field_name}') in self.fields:
                    return True
        return False

    def has_fields(self, field_names: Iterable[str]) -> bool:
        """
        Table.has_field() for Iterable of field names.

        :param field_names: Iterable of field_names.
        :return: True - all given field names are present in this Table.
        """
        for f in field_names:
            if not self.has_field(f):
                return False
        return True

    @property
    def is_real(self) -> bool:
        """
        Is this Table really contained in DBase or just a complex structure of other Tables.

        :return: True - Table is present in DBase, False - Table is a composition of real Tables.
        """
        return self._is_real

    @property
    def name(self) -> str:
        """Current Table's name. Not supposed to match SQL table name."""
        return self._name

    @property
    def query(self) -> str:
        """
        This Table query for DBase.

        This is SQL command used to get current Table's structure from DBase.

        :return: str of query reference
        """
        return self._query

    @property
    def binded(self) -> set['Table']:
        """
        All tables binded with this Table.

        'Binded' means that 'binded table' is present in DBase as real table and is used to make queries to this Table.

        :return: set of binded Tables
        """
        return self._binded

    @property
    def db(self) -> '_Base.DBase':
        """Database which contains this table."""
        return self._db

    @property
    def fields(self) -> dict['TableField']:
        """All fields of current Table."""
        return self._fields.copy()

    @property
    def foreign_keys(self) -> dict[str, 'TableFK']:
        """All foreign keys of current Table."""
        return self._foreign_keys

    @property
    def foreign_tables(self) -> set['Table']:
        """All Tables to whom current Table is connected by foreign keys."""
        return self._foreign_tables.copy()

    def catch_fk_connection(self, other: 'Table') -> 'TableFK':
        """
        Find Foreign Key that connects two tables.

        :param other: other Table.
        :return: TableFK that represents connection between this Table and other Table.
        """
        if maybe := self.binded.intersection(other.foreign_tables):
            master = self
            slave = other
        elif maybe := other.binded.intersection(self.foreign_tables):
            master = other
            slave = self
        else:
            raise KeyError(f"{self} and {other} are not connected by foreign key")

        for fk, fkey in slave.foreign_keys.items():
            try_master_ref = f'{fkey.master_field.table.name}.{fkey.master_field.name}'
            if master.has_field(try_master_ref):
                return fkey

    def join(self, other: 'Table', join: str, self_field: 'TableField', other_field: 'TableField') -> 'Table':
        """
        Make new Table, that is composition of current and other Tables, JOINED by fields.
        :param other: other Table to JOIN
        :param join: JOIN type: "INNER", "LEFT" etc
        :param self_field: field of current Table to use in JOIN comparison
        :param other_field: field of other Table to use in JOIN comparison
        :return:
        """
        name = f"{self.name}_{join}_{other.name}"

        binded = self.binded.union(other.binded)
        query = f'{self.query} {join} JOIN {other.query} ON {self_field.full_name} = {other_field.full_name}'

        return Table(name, self.db, table_query=f'({query})', binded_tables=binded)

    def DROP(self) -> None:
        """
        Drop current table from DBase.
        """
        self._db.drop(self.name)

    def INSERT(self, values: Mapping[str, Any] | Sequence):
        """
        Insert new row into this Table with specified values.

        Gaps in values are not supported.
        Only Real Tables supported.

        if <tuple> is passed:
        - Values order must match this Table fields order. See Table.fields property.
        - If Table Primary Key is AUTOINCREMENT you have not to use dict.

        if <dict> is passed:
        - keys are field names, values are values.

        :param values: <tuple | dict> definition for new row.
        """
        if not self.is_real:
            raise TypeError(f'Only Real Tables supported. {self} is a query composition of {self.binded} tables')

        if isinstance(values, tuple):
            fields = tuple(field.name for field in tuple(self._fields.values())[:len(values)])
        elif isinstance(values, dict):
            fields = tuple(values.keys())
            values = tuple(values.values())
        else:
            raise TypeError(f'expected <tuple> or <dict>, got {type(values)}')

        for f in fields:
            if not self.has_field(f):
                raise KeyError(f'Table {self} does not have field {f}')

        self.db.insert(self.name, fields, values)

    def SELECT(self, field_names: Union[slice, tuple, str, 'aggregate.Aggregate']) -> '_Query.SelectQuery':
        """
        Create SelectQuery for Table.

        :param field_names: Table field names to select
        :return: new SelectQuery
        """
        if isinstance(field_names, slice):
            field_names = tuple(self.fields.keys())
        if not isinstance(field_names, tuple):
            field_names = (field_names,)

        fields = []
        for f in field_names:
            if isinstance(f, aggregate.Aggregate):
                fields.append(f.compile(self))
            else:
                fields.append(self.field_by_name(f))

        return _Query.SelectQuery(self, fields)

    def AND(self, other: 'Table') -> 'Table':
        """
        Make cartisian prodyts of tables.

        :param other: other Table for production
        :return: new Table with is_real=False property
        """
        name = f'{self.name}_x_{other.name}'
        binded = self.binded.union(other.binded)
        query = f'({self.query} CROSS JOIN {other._query})'

        return Table(name, self._db, table_query=query, binded_tables=binded)

    def INNER(self, other: 'Table') -> 'Table':
        """
        INNER JOIN two tables by foreign key.

        :param other: other Table to join
        :return: new Table with is_real=False property
        """
        fk_connection = self.catch_fk_connection(other)

        master = fk_connection.master_field.table
        slave = fk_connection.slave_field.table

        master_ref = fk_connection.master_field
        slave_ref = fk_connection.slave_field

        return self.join(other, 'INNER', master_ref, slave_ref)

    def LEFT(self, other: 'Table') -> 'Table':
        """
        LEFT JOIN two tables by foreign key.

        If you want a RIGHT JOIN, just LEFT JOIN tables in reversed order.

        :param other: other Table to exclude from this Table.
        :return:new Table with is_real=False property
        """
        fk_connection = self.catch_fk_connection(other)

        if fk_connection.master_field.table == self:
            self_ref = fk_connection.master_field
            other_ref = fk_connection.slave_field
        else:
            self_ref = fk_connection.slave_field
            other_ref = fk_connection.master_field

        return self.join(other, 'LEFT', self_ref, other_ref)

    def FULL(self, other: 'Table') -> 'Table':
        """
        FULL JOIN two tables by foreign key.

        :param other: other Tabl to join.
        :return: new Table with is_real=False property
        """
        fk_connection = self.catch_fk_connection(other)
        master = fk_connection.master_field.table
        slave = fk_connection.slave_field.table

        master_ref = fk_connection.master_field
        slave_ref = fk_connection.slave_field

        return self.join(other, 'FULL', master_ref, slave_ref)

    def __getitem__(self, field_names: Union[slice, tuple, str, 'aggregate.Aggregate']) -> '_Query.SelectQuery':
        """
        Create SelectQuery for Table.

        :param field_names: Table field names to select
        :return: new SelectQuery
        """
        return self.SELECT(field_names)

    def __mul__(self, other: 'Table') -> 'Table':
        """
        Make cartisian prodyts of tables.

        :param other: other Table for production
        :return: new Table with is_real=False property
        """
        return self.AND(other)

    def __xor__(self, other: 'Table') -> 'Table':
        """
        FULL JOIN two tables by foreign key.

        :param other: other Tabl to join.
        :return: new Table with is_real=False property
        """
        return self.FULL(other)

    def __sub__(self, other: 'Table') -> 'Table':
        """
        LEFT JOIN two tables by foreign key.

        If you want a RIGHT JOIN, just LEFT JOIN tables in reversed order.

        :param other: other Table to exclude from this Table.
        :return:new Table with is_real=False property
        """
        return self.LEFT(other)

    def __and__(self, other: 'Table') -> 'Table':
        """
        INNER JOIN two tables by foreign key.

        :param other: other Table to join
        :return: new Table with is_real=False property
        """
        return self.INNER(other)

    def __lshift__(self, values: Mapping[str, Any] | Sequence) -> None:
        """
        Insert new row into this Table with specified values.

        Gaps in values are not supported.
        Only Real Tables supported.

        if <tuple> is passed:
        - Values order must match this Table fields order. See Table.fields property.
        - If Table Primary Key is AUTOINCREMENT you have not to use dict.

        if <dict> is passed:
        - keys are field names, values are values.

        :param values: <tuple | dict> definition for new row.
        """
        self.INSERT(values)

    def __repr__(self) -> str:
        return f'Table<{self.name} of {self.db.name}, {"Real" if self.is_real else "Composition"}>'

    def __eq__(self, other: 'Table'):
        return (self.query == other.query) and (self.db.name == other.db.name)

    def __hash__(self):
        return hash((self.query, self.db.name))


class TableField:
    """TableField object, that represents some Table field."""
    def __init__(self, i: int, name: str, typ: str, table_obj: Table,
                 constraints: Iterable['_Constr.FieldConstraint'] = None):
        self.id = i
        self.name = name
        self.type = typ
        self.table = table_obj
        self.constraints = list(constraints) if constraints else list()

    @property
    def full_name(self) -> str:
        """Full name means <Table name>.<Field name>"""
        return self.table.field_from_name(self.name)

    @property
    def is_primary(self) -> bool:
        for c in self.constraints:
            if isinstance(c, _Constr.Primary):
                return True
        return False

    @property
    def is_nullable(self) -> bool:
        for c in self.constraints:
            if isinstance(c, _Constr.NotNull):
                return False
        return True

    @property
    def is_foreign(self) -> bool:
        for c in self.constraints:
            if isinstance(c, _Constr.Foreign):
                return True
        return False

    @property
    def is_checked(self) -> bool:
        for c in self.constraints:
            if isinstance(c, _Constr.Check):
                return True
        return False

    def __repr__(self) -> str:
        return f'Field<{self.id}, {self.name}, {self.type} of {self.table}, {self.constraints}>'

    def __eq__(self, other: 'TableField') -> bool:
        return (self.name == other.name) and (self.table == other.table)

    def __hash__(self):
        return hash((self.name, self.table.name, self.table.db.name))


class CalculatedField:
    def __init__(self, field: 'TableField', function: str):
        self.field = field
        self.function = function

    @property
    def full_name(self) -> str:
        return f'{self.function}({self.field.full_name})'

    @property
    def id(self) -> int:
        return self.field.id

    @property
    def table(self) -> 'Table':
        return self.field.table

    @property
    def type(self) -> str:
        return self.field.type

    @property
    def name(self):
        return self.field.name

    def __repr__(self) -> str:
        return f'CalculatedField<{self.function} from {self.field}>'

    def __eq__(self, other: Union['CalculatedField', 'TableField']) -> bool:
        equality = (self.name == other.name) and (self.table == other.table)
        if isinstance(other, CalculatedField):
            equality = equality and (self.function == other.function)

        return equality

    def __hash__(self):
        return hash((self.name, self.table.name, self.table.db.name, self.function))


class TableFK:
    """TableFK object represents connection between two TableFields by foreign key constraint."""
    def __init__(self, master_field: TableField, slave_field: TableField):
        self._master_field = master_field
        self._slave_field = slave_field

    @property
    def master_field(self) -> 'TableField':
        """Field of table which is Master in foreign key connection."""
        return self._master_field

    @property
    def slave_field(self) -> 'TableField':
        """Field of table which is Slave in foreign key connection."""
        return self._slave_field

    def __repr__(self) -> str:
        return f'TableFK<{self.slave_field} -> {self.master_field}>'

    def __eq__(self, other: 'TableFK'):
        return (self.master_field == other.master_field) and (self.slave_field == other.slave_field)

    def __hash__(self):
        return hash((self.master_field, self.slave_field))