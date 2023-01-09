from __future__ import annotations

import warnings
from typing import Union, AnyStr, Any

import influxdb_datalogger

from .tag_operator import TagOperator
from .functions import QueryFunction


class Compiler:

    def __init__(self):
        self.components = list()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    class Parenthesise:
        def __init__(self, compiler: Compiler):
            self.compiler = compiler
            self.components = list()
            pass

        def __enter__(self):
            self.components.append(self.compiler._START_PARENTHESIS())
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.components.append(self.compiler._END_PARENTHESIS())

        def AND(self):
            self.components.append(self.compiler._AND(self.AND.__name__))
            return self

        def OR(self):
            self.components.append(self.compiler._OR(self.OR.__name__))
            return self

        def tag(self, key, operator, value):
            self.components.append(self.compiler.tag(key, operator, value))
            return self

    def _add_clause(self, clause: str, full_clause: str = None):
        assert clause not in self.components
        if full_clause:
            self.components.append(full_clause)
            return full_clause
        else:
            self.components.append(clause)
            return clause

    def PARENTHESIS(self):
        return Compiler.Parenthesise(self)

    def START_PARENTHESIS(self):
        self._START_PARENTHESIS()
        return self

    def _START_PARENTHESIS(self):
        c = "("
        self.components.append(c)
        return c

    def END_PARENTHESIS(self):
        self._END_PARENTHESIS()
        return self

    def _END_PARENTHESIS(self):
        c = ")"
        self.components.append(c)
        return c

    def SELECT(self, full_clause=None):
        c = Compiler.SELECT.__name__
        self._SELECT(c, full_clause=full_clause)
        return self

    def _SELECT(self, c, full_clause):
        return self._add_clause(c, full_clause)

    def DELETE(self, full_clause=None):
        c = Compiler.DELETE.__name__
        self._DELETE(c, full_clause=full_clause)
        return self

    def _DELETE(self, c, full_clause):
        return self._add_clause(c, full_clause)

    def FROM(self, full_clause: str = None):
        c = Compiler.FROM.__name__
        self._FROM(c, full_clause=full_clause)
        return self

    def _FROM(self, c, full_clause):
        return self._add_clause(c, full_clause)

    def WHERE(self, full_clause: str = None):
        c = Compiler.WHERE.__name__
        self._add_clause(c, full_clause=full_clause)
        return self

    def _WHERE(self, c, full_clause):
        return self._add_clause(c, full_clause)

    def GROUP_BY(self, full_clause: str = None):
        """
        Creates a GROUP BY clause, or adds a full GROUP BY clause that was pre-built
        :param full_clause: Optional argument for a fully compiled GROUP BY clause.
        :return:
        """
        c = Compiler.GROUP_BY.__name__.replace("_", " ")
        self._add_clause(c, full_clause=full_clause)
        return self

    def _GROUP_BY(self, c, full_clause):
        return self._add_clause(c, full_clause)

    def LIMIT(self, lim: int = None, full_clause: str = None):
        if not lim:
            assert full_clause is not None, "No limit, nor full clause has been configured; This is not allowed"
        else:
            assert isinstance(lim, int) and lim > 0, "The limit must be a positive integer above 0"
        c = f"{Compiler.LIMIT.__name__} {lim}"
        self._LIMIT(c, full_clause)
        return self

    def _LIMIT(self, c, full_clause):
        return self._add_clause(c, full_clause=full_clause)

    def AND(self):
        c = Compiler.AND.__name__
        self._AND(c)
        return self

    def _AND(self, c):
        self.components.append(c)
        return c

    def OR(self):
        c = Compiler.OR.__name__
        self._OR(c)
        return self

    def _OR(self, c):
        self.components.append(c)
        return c

    def field(self, *fields: Union[influxdb_datalogger.Field, AnyStr], query_function: QueryFunction = None):
        assert len(fields) <= 1 or not query_function, "You've passed more than 1 field, and a query function. This is not permitted."
        _fields = [f'"{f}"' for f in fields] or ["*"]
        s = ",".join(_fields)
        if query_function:
            s = f"""{query_function}({s})"""
        self.components.append(s)
        return self

    def measurement(self, *measurement: Union[influxdb_datalogger.Measurement, AnyStr]):
        self._measurement(*measurement)
        return self

    def _measurement(self, *measurement: Union[influxdb_datalogger.Measurement, AnyStr]):
        measurement = ",".join([f"\"{m}\"" for m in measurement])
        measurement = measurement or "/.*/"
        self.components.append(measurement)
        return measurement

    def tag(self, key: Union[influxdb_datalogger.Tag, AnyStr], operator: Union[TagOperator, AnyStr], value: Any):
        assert isinstance(operator, (TagOperator, str)), f"'operator' should be of type {TagOperator} or {str}"
        if isinstance(operator, str):
            valid_operators = ("=", "<", ">", "!=", "<=", ">=")
            assert operator in valid_operators, f"Operator '{operator}' is not valid. Pick one of {valid_operators} or use class {TagOperator} from the querier lib instead"
        self._tag(key, operator, value)
        return self

    def _tag(self, key: Union[influxdb_datalogger.Tag, AnyStr], operator: Union[TagOperator, AnyStr], value: Any):
        t = f"""\"{key}\" {operator} \'{value}\'"""
        self.components.append(t)
        return t

    def group(self, *tags: Union[influxdb_datalogger.Tag, AnyStr]):
        self._group(*tags)
        return self

    def _group(self, *tags: Union[influxdb_datalogger.Tag, AnyStr]):
        tags = tags or "*"
        tags = ",".join([f"\"{m}\"" for m in tags])
        if "*" in tags and len(tags) > 1:
            warnings.warn(f"You've passed more groups along with '*'. All other groups will be ignored since they are technically included with '*'. You should change the usage of this function ({self.group.__name__})")
            self.components.append("*")
        else:
            self.components.append(tags)
        return tags

    def compile(self) -> str:
        return " ".join(self.components)
