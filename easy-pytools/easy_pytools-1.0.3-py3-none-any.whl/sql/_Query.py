from typing import Iterable, Union, Type
from . import _Table
from . import _Where
from . import _internal
from . import _exceptions


class UpdateQuery:
    """
    UpdateQuert object to perform update on table.
    """
    def __init__(self, selection: 'SelectQuery', values: tuple | dict):
        self._target = selection.source
        self._fields = selection.fields
        self._values = values
        self._where = selection.where_condition
        self._having = selection.having_condition
        self._group = selection.group_fields

        if (not self._target.is_real) and (self._where is not None):
            raise _exceptions.TableIsNotReal(self._target.name)

        if not isinstance(values, dict) and ((lv := len(values)) != (lf := len(self._fields))):
            raise ValueError(f'All fields from selection have to be initialized in UPDATE query, but only {lv} of {lf} are.')

    def __call__(self, commit=True) -> None:
        """
        Make SQL UPDATE Query, which is presented by current object.

        :param commit: True means to commit changes to database after query success.
        """
        query = str(self)
        self._target.db.query(query, commit=commit)

    def __str__(self) -> str:
        if isinstance(self._values, tuple):
            fields = (f.name for f in self._fields)
            values = self._values
        elif isinstance(self._values, dict):
            fields = (self._target.field_by_name(f).name for f in self._values.keys())
            values = self._values.values()
        else:
            raise TypeError(f'expected <dict> or <tuple> for value assignment, got {type(self._values)}')

        update = f'''UPDATE
        {self._target.name} SET {",".join(fields)} = ({",".join(_internal.proper_values(values))})'''
        where = f' WHERE {self._where}' if self._where is not None else ""
        group = f' GROUP BY {",".join(f.full_name for f in self._group)}' if self._group else ""
        having = f' HAVING {self._having}' if self._having else ""
        return f'{update}{where}{group}{having};'

    def __repr__(self) -> str:
        return str(self)


class SelectQuery:
    """
    SelectQuery object to perform SELECT queries and its compositions.
    """
    def __init__(self, source: '_Table.Table', fields: Iterable['_Table.TableField']):
        self._source = source
        self._fields = tuple(fields)
        self._distinct = False
        self._where = None
        self._having = None
        self._body = None
        self._union_comparator = _Where.WhereAND
        self._group: tuple['_Table.TableField'] = tuple()
        self._order: tuple['_Table.TableField'] = tuple()


    @property
    def union_comparator(self) -> Type['_Where.WhereComposition']:
        """Comparator type which will be used on further conditions composition for this query."""
        return self._union_comparator

    @property
    def is_distinct(self) -> bool:
        """Is this query DISTINCT or not."""
        return self._distinct

    @property
    def where_condition(self) -> Type['_Where.Where']:
        return self._where

    @property
    def having_condition(self) -> Type['_Where.Where']:
        return self._having

    @property
    def group_fields(self) -> tuple['_Table.TableField']:
        return self._group

    @property
    def order_fields(self) -> tuple['_Table.TableField']:
        return self._order

    @property
    def source(self) -> '_Table.Table':
        """Source Table object to SELECT from."""
        return self._source

    @property
    def fields(self) -> tuple['_Table.TableField']:
        """Fields used in current selection."""
        return self._fields

    @property
    def body(self):
        """Last query operation result. Used for caching."""
        return self._body

    @property
    def distinct(self) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but selection will be DISTINCT."""
        new = self.copy()
        new._distinct = True
        return new

    @property
    def OR(self) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but newly added selection conditions will be added with OR."""
        new = self.copy()
        new._union_comparator = _Where.WhereOR
        return new

    @property
    def AND(self) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but newly added selection conditions will be added with AND."""
        new = self.copy()
        new._union_comparator = _Where.WhereAND
        return new

    def WHERE(self, values: list | tuple, comparison: type, union: type) -> 'SelectQuery':
        """
        Make new SelectQuery, which is copy of current, but add new selection condition.

        :param values: condition description.
        :param comparison: Where class reference which represents how values would be checked.
        :param union: WhereComposition class reference which represents how all checks will be composited.
        :return: new SelectQuery object.
        """
        if isinstance(values, list):
            where_type = _Where.WhereAND
        elif isinstance(values, tuple):
            where_type = _Where.WhereOR
        else:
            raise TypeError(f'expected <tuple> for AND or <list> for OR, got {type(values)}')

        new_wheres = []
        new_havings = []
        for value, field in zip(_internal.proper_values(values), self.fields):
            if (value == tuple()) or (value == list()):
                continue
            if isinstance(value, tuple):
                new_condition = _Where.WhereOR(*(comparison(field, v) for v in _internal.proper_values(value)))
            elif isinstance(value, list):
                new_condition = _Where.WhereAND(*(comparison(field, v) for v in _internal.proper_values(value)))
            else:
                new_condition = comparison(field, value)

            if isinstance(field, _Table.CalculatedField):
                new_havings.append(new_condition)
            else:
                new_wheres.append(new_condition)

        where = union(self._where, where_type(*new_wheres)) if self._where is not None else where_type(*new_wheres)
        having = union(self._having, where_type(*new_havings)) if self._having is not None else where_type(*new_havings)

        new = self.copy()
        new._where = where if new_wheres else None
        new._having = having if new_havings else None
        return new

    def WHERE_EQ(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on equalities."""
        return self.WHERE(values, _Where.WhereEq, self._union_comparator)

    def WHERE_GT(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on greaters."""
        return self.WHERE(values, _Where.WhereGt, self._union_comparator)

    def WHERE_LT(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on lessers."""
        return self.WHERE(values, _Where.WhereLt, self._union_comparator)

    def GROUPBY(self, fields: tuple) -> 'SelectQuery':
        """Make new SelectQuery, which copy of current, but with grouping fields."""
        fields = tuple(self._source.field_by_name(v) for v in fields)
        new = self.copy()
        new._group = fields
        return new

    def ORDERBY(self, fields: tuple) -> 'SelectQuery':
        fields = tuple(self._source.field_by_name(v) for v in fields)
        new = self.copy()
        new._order = fields
        return new

    def UPDATE(self, values: tuple | list) -> 'UpdateQuery':
        """Make new UpdateQuery, that affects rows and fields selected with current SelectQuery."""
        return UpdateQuery(self, values)

    def __eq__(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on equalities."""
        return self.WHERE_EQ(values)

    def __gt__(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on greaters."""
        return self.WHERE_GT(values)

    def __lt__(self, values: list | tuple) -> 'SelectQuery':
        """Make new SelectQuery, which is copy of current, but with additional selection condition on lessers."""
        return self.WHERE_LT(values)

    def __mod__(self, fields: tuple) -> 'SelectQuery':
        """Make new SelectQuery, which copy of current, but with grouping fields."""
        return self.GROUPBY(fields)

    def __div__(self, fields: tuple) -> 'SelectQuery':
        return self.ORDERBY(fields)

    def __lshift__(self, values: tuple | dict) -> 'UpdateQuery':
        """Make new UpdateQuery, that affects rows and fields selected with current SelectQuery."""
        return self.UPDATE(values)

    def __call__(self) -> list[tuple]:
        """
        Get result of SQL query, which is presented by current object.

        :return: select SQL query result.
        """
        query = str(self)
        self._body = self._source.db.query(query, commit=False).fetchall()

        return self._body

    def __str__(self):
        select = f'''SELECT {"DISTINCT" if self._distinct else ""}
        {",".join(f.full_name for f in self.fields)} 
        FROM {self.source.query}'''
        where = f' WHERE {self._where}' if self._where else ""
        group = f' GROUP BY {",".join(f.full_name for f in self._group)}' if self._group else ""
        order = f' ORDER BY {",".join(f.full_name for f in self._order)}' if self._order else ""
        having = f' HAVING {self._having}' if self._having else ""

        query = f'{select}{where}{group}{having}{order};'
        return query

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> 'SelectQuery':
        new = SelectQuery(self._source, self._fields)
        new._distinct = self._distinct
        new._where = self._where
        new._having = self._having
        new._group = self._group
        new._order = self._order
        new._union_comparator = self._union_comparator

        return new
