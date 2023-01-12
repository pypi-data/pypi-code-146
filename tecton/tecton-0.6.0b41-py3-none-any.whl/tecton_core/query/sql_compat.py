import enum
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pypika
from pypika import AliasedQuery
from pypika import analytics
from pypika import CustomFunction
from pypika import Field
from pypika import Interval
from pypika import Table
from pypika.dialects import MySQLQuery
from pypika.dialects import PostgreSQLQuery
from pypika.functions import Cast
from pypika.functions import DateAdd
from pypika.queries import Selectable
from pypika.terms import AnalyticFunction
from pypika.terms import Function
from pypika.terms import LiteralValue
from pypika.terms import Term
from pypika.utils import format_alias_sql

from tecton_core import conf
from tecton_core.data_types import DataType


class CaseSensitiveSnowflakeQuery(pypika.queries.Query):
    @classmethod
    def _builder(cls, **kwargs: Any) -> "CaseSensitiveSnowflakeQueryBuilder":
        return CaseSensitiveSnowflakeQueryBuilder(**kwargs)


class CaseSensitiveSnowflakeQueryBuilder(pypika.dialects.SnowflakeQueryBuilder):
    QUOTE_CHAR = '"'


class CustomQuery(pypika.queries.QueryBuilder):
    """
    Defines a custom-query class. It's needed for us to wrap some user-defined sql string from transformations in a QueryBuilder object.
    """

    def __init__(self, sql: str):
        super().__init__(self)
        self.sql = sql
        self.withs: List[Selectable] = []

    def with_(self, selectable: Selectable, name: str):
        """
        overrides QueryBuilder.with_
        """
        t = AliasedQuery(name, selectable)
        self.withs.append(t)
        return self

    def get_sql(self, with_alias: bool = False, subquery: bool = False, **kwargs):
        """
        overrides QueryBuilder.get_sql
        """
        sql = ""
        if self.withs:
            sql += "WITH " + ",".join(
                clause.name + " AS (" + clause.get_sql(subquery=False, with_alias=False, **kwargs) + ") "
                for clause in self.withs
            )
        sql += self.sql
        if with_alias:
            self.alias = "sq0"
            sql = f"({sql})"
            return format_alias_sql(sql, self.alias or self._table_name, **kwargs)
        return sql


class LastValue(analytics.LastValue):
    """
    Fixed version of pypika's LastValue to handle Snowflake and Athena wanting "ignore nulls"
     to be outside the parens of the window func, and Spark using a bool param.
    """

    def get_special_params_sql(self, **kwargs: Any) -> Optional[str]:
        if dialect() == Dialect.SPARK:
            # see: https://docs.databricks.com/sql/language-manual/functions/last_value.html
            # for sparkSQL syntax
            return f", {self._ignore_nulls}"
        # Snowflake does not support adding a function param to indicate "ignore nulls"
        # It looks like LAST_VALUE(...) IGNORE NULLS OVER(...)
        # see: https://docs.snowflake.com/en/sql-reference/functions/last_value.html
        # Nor does Athena - Athena docs don't make this clear though.
        else:
            return None

    def get_function_sql(self, **kwargs: Any) -> str:
        if dialect() == Dialect.SPARK:
            return super(LastValue, self).get_function_sql(**kwargs)
        else:
            function_sql = super(AnalyticFunction, self).get_function_sql(**kwargs)
            partition_sql = self.get_partition_sql(**kwargs)

            sql = function_sql
            if self._ignore_nulls:
                sql += " IGNORE NULLS"
            if self._include_over:
                sql += " OVER({partition_sql})".format(partition_sql=partition_sql)
            return sql


class Dialect(str, enum.Enum):
    SNOWFLAKE = "snowflake"
    ATHENA = "athena"
    SPARK = "spark"


def dialect() -> Dialect:
    # TODO(Daryl) - infer the sql dialect from the fv itself,
    # We just use the conf for now as athena transformations are still under development.
    d = conf.get_or_none("SQL_DIALECT")
    try:
        return Dialect(d)
    except:
        raise Exception(f"Unsupported sql dialect: set SQL_DIALECT to {[x.value for x in Dialect]}")


def Query():
    if dialect() == Dialect.SNOWFLAKE:
        return CaseSensitiveSnowflakeQuery
    elif dialect() == Dialect.SPARK:
        # Spark (similar to HiveSQL) uses backticks like MySQL
        return MySQLQuery
    else:
        # Athena (similar to PrestoSQL) uses doublequotes like Postgres
        return PostgreSQLQuery


# Spark, Athena, and Snowflake use different versions of structs.
class Struct(Function):
    def __init__(self, dialect: Dialect, *args, **kwargs):
        if dialect == Dialect.SPARK:
            f = "struct"
        elif dialect == Dialect.ATHENA:
            f = "row"
        elif dialect == Dialect.SNOWFLAKE:
            f = "array_construct"
        else:
            raise NotImplementedError
        super(Struct, self).__init__(f, *args, **kwargs)


def struct(field_names: List[str]) -> Term:
    fields = [Field(n) for n in field_names]
    return Struct(dialect(), *fields)


def default_case(field_name: str) -> str:
    # Snowflake defaults to uppercase
    if dialect() == Dialect.SNOWFLAKE:
        return field_name.upper()
    else:
        return field_name


def struct_extract(name: str, field_names: List[str], aliases: List[str], schema: Dict[str, DataType]) -> List[Field]:
    """
    Returns list of fields that pull out all `field_names` from the struct object, and alias them to `aliases`
    """
    if dialect() == Dialect.SPARK:
        assert len(field_names) == len(aliases)
        return [getattr(Table(name), (field)).as_(alias) for (field, alias) in zip(field_names, aliases)]
    elif dialect() == Dialect.ATHENA:
        return [getattr(Table(name), f"field{idx}").as_(aliases[idx]) for idx in range(len(aliases))]
    elif dialect() == Dialect.SNOWFLAKE:
        get = CustomFunction("get", ["array", "idx"])
        res = []
        for idx in range(len(aliases)):
            val = get(Field(name), idx)
            if field_names[idx] in schema:
                feature_type = schema[field_names[idx]].sql_type
                val = Cast(val, feature_type)
            res.append(val.as_(aliases[idx]))
        return res
    else:
        raise NotImplementedError


def to_timestamp(time_str: str) -> Term:
    if dialect() == Dialect.SNOWFLAKE or dialect() == Dialect.SPARK:
        c = CustomFunction("to_timestamp", ["time_str"])
    else:
        c = CustomFunction("from_iso8601_timestamp", ["time_str"])
    return c(time_str)


def date_add(interval: str, amount: int, time_field: Term) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        # snowflake uses dateadd rather than date_add; https://docs.snowflake.com/en/sql-reference/functions/dateadd.html
        c = CustomFunction("dateadd", ["interval", "amount", "time_field"])
        # LiteralValue will not put quotes around.
        # So we get dateadd(second, ...)
        interval = LiteralValue(interval)
    elif dialect() == Dialect.SPARK:
        if interval == "second":
            return time_field + Interval(seconds=amount)
        else:
            raise NotImplementedError
    else:
        c = DateAdd
        # For Athena, see: https://trino.io/docs/current/functions/datetime.html
        interval = f"'{interval}'"
    return c(interval, amount, time_field)


def to_unixtime(timestamp: Term) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        c = CustomFunction("date_part", ["epoch", "timestamp"])
        return c(Field("epoch_second"), timestamp)
    elif dialect() == Dialect.SPARK:
        c = CustomFunction("unix_timestamp", ["timestamp"])
        return c(timestamp)
    else:
        c = CustomFunction("to_unixtime", ["timestamp"])
        return c(timestamp)


def from_unixtime(unix_timestamp: Term) -> Term:
    if dialect() == Dialect.SNOWFLAKE:
        c = CustomFunction("to_timestamp", ["unix_timestamp"])
        return c(unix_timestamp)
    elif dialect() == Dialect.ATHENA:
        c = CustomFunction("from_unixtime", ["unix_timestamp"])
        return c(unix_timestamp)
    else:
        c = CustomFunction("from_unixtime", ["unix_timestamp"])
        return Cast(c(unix_timestamp), "timestamp")
