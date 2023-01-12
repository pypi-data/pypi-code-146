"""Integration between SQLAlchemy and ClickZetta."""

from __future__ import absolute_import
from __future__ import unicode_literals

from decimal import Decimal
import random
import operator
import uuid

import clickzetta.dbapi
from clickzetta import dbapi
from clickzetta.table import Table

import sqlalchemy
import sqlalchemy.sql.expression
import sqlalchemy.sql.functions
import sqlalchemy.sql.sqltypes
import sqlalchemy.sql.type_api
from sqlalchemy.exc import NoSuchTableError
from sqlalchemy import util
from sqlalchemy.sql.compiler import (
    SQLCompiler,
    GenericTypeCompiler,
    DDLCompiler,
    IdentifierPreparer,
)
from sqlalchemy.sql.sqltypes import Integer, String, NullType, Numeric
from sqlalchemy.engine.default import DefaultDialect, DefaultExecutionContext
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.selectable import CTE
from sqlalchemy.sql import elements, selectable
import re

from .parse_url import parse_url
from . import _helpers, _types

FIELD_ILLEGAL_CHARACTERS = re.compile(r"[^\w]+")
TABLE_VALUED_ALIAS_ALIASES = "clickzetta_table_valued_alias_aliases"


def assert_(cond, message="Assertion failed"):  # pragma: NO COVER
    if not cond:
        raise AssertionError(message)


class ClickZettaIdentifierPreparer(IdentifierPreparer):

    def __init__(self, dialect):
        super(ClickZettaIdentifierPreparer, self).__init__(
            dialect,
            initial_quote="`",
        )

    def quote_column(self, value):

        parts = value.split(".")
        return ".".join(self.quote_identifier(x) for x in parts)

    def quote(self, ident, force=None, column=False):

        force = getattr(ident, "quote", None)
        if force is None or force:
            return self.quote_column(ident) if column else self.quote_identifier(ident)
        else:
            return ident

    def format_label(self, label, name=None):
        name = name or label.name
        if not name[0].isalpha() and name[0] != "_":
            name = "_" + name

        name = FIELD_ILLEGAL_CHARACTERS.sub("_", name)

        result = self.quote(name)
        return result


class ClickZettaExecutionContext(DefaultExecutionContext):
    def create_cursor(self):
        # Set arraysize
        c = super(ClickZettaExecutionContext, self).create_cursor()
        if self.dialect.arraysize:
            c.arraysize = self.dialect.arraysize
        return c

    def get_insert_default(self, column):
        if isinstance(column.type, Integer):
            return random.randint(-9223372036854775808, 9223372036854775808)
        elif isinstance(column.type, String):
            return str(uuid.uuid4())

    __remove_type_from_empty_in = _helpers.substitute_string_re_method(
        r"""
        \sIN\sUNNEST\(\[\s               # ' IN UNNEST([ '
        (
        (?:NULL|\(NULL(?:,\sNULL)+\))\)  # '(NULL)' or '((NULL, NULL, ...))'
        \s(?:AND|OR)\s\(1\s!?=\s1        # ' and 1 != 1' or ' or 1 = 1'
        )
        (?:[:][A-Z0-9]+)?                # Maybe ':TYPE' (e.g. ':INT64')
        \s\]\)                           # Close: ' ])'
        """,
        flags=re.IGNORECASE | re.VERBOSE,
        repl=r" IN(\1)",
    )

    @_helpers.substitute_re_method(
        r"""
        \sIN\sUNNEST\(\[\s       
        (                        
        %\([^)]+_\d+\)s          
        (?:,\s                   
        %\([^)]+_\d+\)s
        )*
        )?
        :([A-Z0-9]+)             
        \s\]\)                   
        """,
        flags=re.IGNORECASE | re.VERBOSE,
    )
    def __distribute_types_to_expanded_placeholders(self, m):
        placeholders, type_ = m.groups()
        if placeholders:
            placeholders = placeholders.replace(")", f":{type_})")
        else:
            placeholders = ""
        return f" IN UNNEST([ {placeholders} ])"

    def pre_exec(self):
        self.statement = self.__distribute_types_to_expanded_placeholders(
            self.__remove_type_from_empty_in(self.statement)
        )


class ClickZettaCompiler(SQLCompiler):
    compound_keywords = SQLCompiler.compound_keywords.copy()
    compound_keywords[selectable.CompoundSelect.UNION] = "UNION DISTINCT"
    compound_keywords[selectable.CompoundSelect.UNION_ALL] = "UNION ALL"

    def __init__(self, dialect, statement, *args, **kwargs):
        if isinstance(statement, Column):
            kwargs["compile_kwargs"] = util.immutabledict({"include_table": False})
        super(ClickZettaCompiler, self).__init__(dialect, statement, *args, **kwargs)

    def visit_insert(self, insert_stmt, asfrom=False, **kw):

        self.inline = False

        return super(ClickZettaCompiler, self).visit_insert(
            insert_stmt, asfrom=False, **kw
        )

    def visit_table_valued_alias(self, element, **kw):

        kw[TABLE_VALUED_ALIAS_ALIASES] = {}
        ret = super().visit_table_valued_alias(element, **kw)
        aliases = kw.pop(TABLE_VALUED_ALIAS_ALIASES)
        if aliases:
            aliases = ", ".join(
                f"{self.preparer.quote(tablename)} {self.preparer.quote(alias)}"
                for tablename, alias in aliases.items()
            )
            ret = f"{aliases}, {ret}"
        return ret

    def _known_tables(self):
        known_tables = set()

        for from_ in self.compile_state.froms:
            if isinstance(from_, Table):
                known_tables.add(from_.name)
            elif isinstance(from_, CTE):
                for column in from_.original.selected_columns:
                    table = getattr(column, "table", None)
                    if table is not None:
                        known_tables.add(table.name)

        return known_tables

    def visit_column(
            self,
            column,
            add_to_result_map=None,
            include_table=True,
            result_map_targets=(),
            **kwargs,
    ):
        name = orig_name = column.name
        if name is None:
            name = self._fallback_column_name(column)

        is_literal = column.is_literal
        if not is_literal and isinstance(name, elements._truncated_label):
            name = self._truncated_identifier("colident", name)

        if add_to_result_map is not None:
            targets = (column, name, column.key) + result_map_targets
            if getattr(column, "_tq_label", None):
                targets += (column._tq_label,)

            add_to_result_map(name, orig_name, targets, column.type)

        if is_literal:
            name = self.escape_literal_column(name)
        else:
            name = self.preparer.quote(name, column=True)
        table = column.table
        if table is None or not include_table or not table.named_with_column:
            return name
        else:
            tablename = table.name
            if isinstance(tablename, elements._truncated_label):
                tablename = self._truncated_identifier("alias", tablename)
            elif TABLE_VALUED_ALIAS_ALIASES in kwargs:
                if tablename not in self._known_tables():
                    aliases = kwargs[TABLE_VALUED_ALIAS_ALIASES]
                    if tablename not in aliases:
                        aliases[tablename] = self.anon_map[
                            f"{TABLE_VALUED_ALIAS_ALIASES} {tablename}"
                        ]
                    tablename = aliases[tablename]

            return self.preparer.quote(tablename) + "." + name

    def visit_label(self, *args, within_group_by=False, **kwargs):
        if within_group_by:
            kwargs["render_label_as_label"] = args[0]
        return super(ClickZettaCompiler, self).visit_label(*args, **kwargs)

    def group_by_clause(self, select, **kw):
        return super(ClickZettaCompiler, self).group_by_clause(
            select, **kw, within_group_by=True
        )

    __sqlalchemy_version_info = tuple(map(int, sqlalchemy.__version__.split(".")))

    __expanding_text = (
        "EXPANDING" if __sqlalchemy_version_info < (1, 4) else "POSTCOMPILE"
    )
    __expanding_conflict = "" if __sqlalchemy_version_info < (1, 4, 27) else "__"

    __in_expanding_bind = _helpers.substitute_string_re_method(
        rf"""
        \sIN\s\(                     
        (
        {__expanding_conflict}\[     
        {__expanding_text}           
        _[^\]]+                      
        \]
        (:[A-Z0-9]+)?                
        )
        \)$                          
        """,
        flags=re.IGNORECASE | re.VERBOSE,
        repl=r" IN UNNEST([ \1 ])",
    )

    def visit_in_op_binary(self, binary, operator_, **kw):
        return self.__in_expanding_bind(
            self._generate_generic_binary(binary, " IN ", **kw)
        )

    def visit_empty_set_expr(self, element_types):
        return ""

    def visit_not_in_op_binary(self, binary, operator, **kw):
        return (
                "("
                + self.__in_expanding_bind(
            self._generate_generic_binary(binary, " NOT IN ", **kw)
        )
                + ")"
        )

    visit_notin_op_binary = visit_not_in_op_binary

    @staticmethod
    def _maybe_reescape(binary):
        binary = binary._clone()
        escape = binary.modifiers.pop("escape", None)
        if escape and escape != "\\":
            binary.right.value = escape.join(
                v.replace(escape, "\\")
                for v in binary.right.value.split(escape + escape)
            )
        return binary

    def visit_contains_op_binary(self, binary, operator, **kw):
        return super(ClickZettaCompiler, self).visit_contains_op_binary(
            self._maybe_reescape(binary), operator, **kw
        )

    def visit_notcontains_op_binary(self, binary, operator, **kw):
        return super(ClickZettaCompiler, self).visit_notcontains_op_binary(
            self._maybe_reescape(binary), operator, **kw
        )

    def visit_startswith_op_binary(self, binary, operator, **kw):
        return super(ClickZettaCompiler, self).visit_startswith_op_binary(
            self._maybe_reescape(binary), operator, **kw
        )

    def visit_notstartswith_op_binary(self, binary, operator, **kw):
        return super(ClickZettaCompiler, self).visit_notstartswith_op_binary(
            self._maybe_reescape(binary), operator, **kw
        )

    def visit_endswith_op_binary(self, binary, operator, **kw):
        return super(ClickZettaCompiler, self).visit_endswith_op_binary(
            self._maybe_reescape(binary), operator, **kw
        )

    def visit_notendswith_op_binary(self, binary, operator, **kw):
        return super(ClickZettaCompiler, self).visit_notendswith_op_binary(
            self._maybe_reescape(binary), operator, **kw
        )

    __placeholder = re.compile(r"%\(([^\]:]+)(:[^\]:]+)?\)s$").match

    __expanded_param = re.compile(
        rf"\({__expanding_conflict}\[" rf"{__expanding_text}" rf"_[^\]]+\]\)$"
    ).match

    __remove_type_parameter = _helpers.substitute_string_re_method(
        r"""
        (VARCHAR|CHAR|DECIMAL)  
        \(                                 
        \s*\d+\s*                          
        (?:,\s*\d+\s*)*                    
        \)
        """,
        repl=r"\1",
        flags=re.VERBOSE | re.IGNORECASE,
    )

    def visit_bindparam(
            self,
            bindparam,
            within_columns_clause=False,
            literal_binds=False,
            skip_bind_expression=False,
            **kwargs,
    ):
        type_ = bindparam.type
        unnest = False
        if (
                bindparam.expanding
                and not isinstance(type_, NullType)
                and not literal_binds
        ):
            if getattr(bindparam, "expand_op", None) is not None:
                assert bindparam.expand_op.__name__.endswith("in_op")  # in in
                bindparam = bindparam._clone(maintain_key=True)
                bindparam.expanding = False
                unnest = True

        param = super(ClickZettaCompiler, self).visit_bindparam(
            bindparam,
            within_columns_clause,
            literal_binds,
            skip_bind_expression,
            **kwargs,
        )

        if literal_binds or isinstance(type_, NullType):
            return param

        if (
                isinstance(type_, Numeric)
                and (type_.precision is None or type_.scale is None)
                and isinstance(bindparam.value, Decimal)
        ):
            t = bindparam.value.as_tuple()

            if type_.precision is None:
                type_.precision = len(t.digits)

            if type_.scale is None and t.exponent < 0:
                type_.scale = -t.exponent

        bq_type = self.dialect.type_compiler.process(type_)
        bq_type = self.__remove_type_parameter(bq_type)

        assert_(param != "%s", f"Unexpected param: {param}")

        if bindparam.expanding:
            assert_(self.__expanded_param(param), f"Unexpected param: {param}")
            if self.__sqlalchemy_version_info < (1, 4, 27):
                param = param.replace(")", f":{bq_type})")

        else:
            m = self.__placeholder(param)
            if m:
                name, type_ = m.groups()
                assert_(type_ is None)
                param = f"%({name}:{bq_type})s"

        if unnest:
            param = f"UNNEST({param})"

        return param

    def visit_getitem_binary(self, binary, operator_, **kw):
        left = self.process(binary.left, **kw)
        right = self.process(binary.right, **kw)
        return f"{left}[OFFSET({right})]"


class ClickZettaTypeCompiler(GenericTypeCompiler):
    def visit_INTEGER(self, type_, **kw):
        return "INT64"

    def visit_SMALLINT(self, type_, **kw):
        return "INT16"

    def visit_integer(self, type_, **kw):
        return "INT32"

    def visit_big_integer(self, type_, **kw):
        return "INT64"

    def visit_BOOLEAN(self, type_, **kw):
        return "BOOL"

    def visit_FLOAT(self, type_, **kw):
        return "FLOAT64"

    def visit_CHAR(self, type_, **kw):
        if (type_.length is not None) and isinstance(
                kw.get("type_expression"), Column
        ):  # column def
            return f"CHAR({type_.length})"
        return "CHAR"

    def visit_VARCHAR(self, type_, **kw):
        if (type_.length is not None) and isinstance(
                kw.get("type_expression"), Column
        ):  # column def
            return f"VARCHAR({type_.length})"
        return "VARCHAR"

    def visit_string(self, type_, **kw):
        return "STRING"

    def visit_ARRAY(self, type_, **kw):
        return "ARRAY<{}>".format(self.process(type_.item_type, **kw))

    def visit_BINARY(self, type_, **kw):
        if type_.length is not None:
            return f"BINARY({type_.length})"
        return "BINARY"

    def visit_DECIMAL(self, type_, **kw):
        if (type_.precision is not None) and isinstance(
                kw.get("type_expression"), Column
        ):  # column def
            if type_.scale is not None:
                suffix = f"({type_.precision}, {type_.scale})"
        else:
            suffix = ""

        return (
                "DECIMAL" + suffix)


class ClickZettaDDLCompiler(DDLCompiler):

    def visit_foreign_key_constraint(self, constraint):
        return None

    def visit_unique_constraint(self, constraint):
        return None


def process_string_literal(value):
    return repr(value.replace("%", "%%"))


class ClickZettaDialect(DefaultDialect):
    name = "clickzetta"
    driver = "clickzetta"
    preparer = ClickZettaIdentifierPreparer
    statement_compiler = ClickZettaCompiler
    type_compiler = ClickZettaTypeCompiler
    ddl_compiler = ClickZettaDDLCompiler
    execution_ctx_cls = ClickZettaExecutionContext
    supports_alter = True
    supports_comments = True
    inline_comments = True
    supports_pk_autoincrement = False
    supports_default_values = False
    supports_empty_insert = False
    supports_multivalues_insert = True
    supports_unicode_statements = True
    supports_unicode_binds = True
    supports_native_decimal = True
    description_encoding = None
    supports_native_boolean = True
    supports_simple_order_by_label = True
    postfetch_lastrowid = False
    preexecute_autoincrement_sequences = False

    def __init__(
            self,
            arraysize=5000,
            *args,
            **kwargs,
    ):
        super(ClickZettaDialect, self).__init__(*args, **kwargs)
        self.arraysize = arraysize
        self.host = None
        self.username = None
        self.driver_name = None
        self.pwd = None
        self.instance_name = None
        self.workspace = None
        self.vc_name = None

    @classmethod
    def dbapi(cls):
        return dbapi

    def create_connect_args(self, url):
        (
            host,
            username,
            driver_name,
            pwd,
            instance_name,
            workspace,
            vc_name,
        ) = parse_url(url)

        self.host = host
        self.arraysize = self.arraysize
        self.username = username
        self.driver_name = driver_name
        self.pwd = pwd
        self.instance_name = instance_name
        self.workspace = workspace
        self.vc_name = vc_name

        client = _helpers.create_clickzetta_client(
            username=self.username,
            password=self.pwd,
            instance_name=self.instance_name,
            workspace=self.workspace,
            vc_name=self.vc_name,
            base_url=self.host,
        )
        return ([], {"client": client})

    def do_rollback(self, dbapi_connection):
        pass

    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return {"constrained_columns": []}

    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    def get_view_names(self, connection, schema=None, **kw):
        return []

    def has_table(self, connection, table_name, schema=None):
        full_table = table_name
        if schema:
            full_table = schema + '.' + table_name
        if isinstance(connection, Engine):
            connection = connection.connect()

        return connection.connection._client.has_table(full_table)

    def get_table_names(self, connection, schema=None, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()
        table_names = connection.connection._client.get_table_names(schema)
        return table_names

    def get_columns(self, connection, table_name, schema=None, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()
        schema = connection.connection._client.get_columns(table_name, schema)
        convert_schema = []
        for field in schema:
            convert_schema.append(
                {
                    'name': field.name,
                    'type': _types.get_clickzetta_column_type(field),
                    'nullable': field.nullable,
                }
            )
        return convert_schema

    def get_schema_names(self, connection, **kw):
        if isinstance(connection, Engine):
            connection = connection.connect()
        schema = connection.connection._client.get_schemas()
        return schema


class unnest(sqlalchemy.sql.functions.GenericFunction):
    def __init__(self, *args, **kwargs):
        expr = kwargs.pop("expr", None)
        if expr is not None:
            args = (expr,) + args
        if len(args) != 1:
            raise TypeError("The unnest function requires a single argument.")
        arg = args[0]
        if isinstance(arg, sqlalchemy.sql.expression.ColumnElement):
            if not isinstance(arg.type, sqlalchemy.sql.sqltypes.ARRAY):
                raise TypeError("The argument to unnest must have an ARRAY type.")
            self.type = arg.type.item_type
        super().__init__(*args, **kwargs)


dialect = ClickZettaDialect

try:
    import alembic  # noqa
except ImportError:
    pass
else:
    from alembic.ddl import impl


    class SqlalchemyClickZettaImpl(impl.DefaultImpl):
        __dialect__ = "clickzetta"
