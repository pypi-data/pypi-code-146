"""Generate type annotated python from SQL."""

from importlib.resources import read_text
from collections import Counter
from dataclasses import dataclass
from typing import Optional, Union

from rich.console import Console
from black import format_str, Mode  # type: ignore
from lark import Lark, Transformer, UnexpectedToken  # type: ignore
from jinja2 import Environment, PackageLoader, StrictUndefined


@dataclass
class Module:
    name: str


@dataclass
class Schema:
    name: str
    sql: str


@dataclass
class VType:
    name: str
    maybe_none: bool


@dataclass
class TypedVar:
    name: str
    type: VType


@dataclass
class Params:
    typed_vars: list[TypedVar]


@dataclass
class RowType:
    name: str
    typed_vars: list[TypedVar]


@dataclass
class Return:
    return_type: Union[VType, RowType]
    returns_one: Optional[bool]


@dataclass
class Query:
    name: str
    params: Optional[Params]
    return_: Optional[Return]
    sql: str


@dataclass
class SqlFile:
    module: Optional[Module]
    schemas: list[Schema]
    queries: list[Query]


class SqlPyGenTransformer(Transformer):
    """Transform the parse tree for code generation."""

    CNAME = str

    def SQL_STRING(self, t):
        return t.strip().rstrip(";").strip()

    def module(self, ts):
        (name,) = ts
        return Module(name)

    def vtype_opt(self, ts):
        (name,) = ts
        return VType(name, True)

    def vtype_not_opt(self, ts):
        (name,) = ts
        return VType(name, False)

    def typed_var(self, ts):
        vname, vtype = ts
        return TypedVar(vname, vtype)

    def typed_vars(self, ts):
        return list(ts)

    def params(self, ts):
        return Params(ts[0])

    def row_type(self, ts):
        rname, tvs = ts
        return RowType(rname, tvs)

    def returnone(self, ts):
        return Return(ts[0], True)

    def returnmany(self, ts):
        return Return(ts[0], False)

    def schema(self, ts):
        name, sql = ts
        return Schema(name, sql)

    def query(self, ts):
        name, sql = ts[0], ts[-1]
        params = None
        return_ = None
        for t in ts[1:-1]:
            if isinstance(t, Params):
                params = t
            elif isinstance(t, Return):
                return_ = t
            else:
                raise ValueError(f"Unexpected child: {t=}")

        return Query(name, params, return_, sql)

    def start(self, ts):
        ret = SqlFile(None, [], [])
        for t in ts:
            if isinstance(t, Module):
                ret.module = t
            elif isinstance(t, Query):
                ret.queries.append(t)
            elif isinstance(t, Schema):
                ret.schemas.append(t)
            else:
                raise ValueError(f"Unexpected child: {t=}")
        return ret


def get_parser() -> Lark:
    """Return the parser."""
    grammar = read_text("sqlpygen", "sqlpygen.lark")
    parser = Lark(grammar, parser="lalr")
    return parser


def py_type(vtype: VType) -> str:
    if vtype.maybe_none:
        return "Optional[%s]" % vtype.name
    else:
        return vtype.name


def fn_params(params: Optional[Params]) -> str:
    if params is None:
        return "connection: ConnectionType"

    xs = [(tv.name, py_type(tv.type)) for tv in params.typed_vars]
    xs = [f"{name}: {type}" for name, type in xs]
    xs = ", ".join(xs)
    xs = "connection: ConnectionType, *," + xs
    return xs


def query_args(params: Params) -> str:
    qa = []
    for tv in params.typed_vars:
        qa.append(f'"{tv.name}": {tv.name}')
    qa = ", ".join(qa)
    qa = f"{{ {qa} }}"
    return qa


def explain_args(params: Params) -> str:
    ea = [f'"{tv.name}": None' for tv in params.typed_vars]
    ea = ", ".join(ea)
    ea = f"{{ {ea} }}"
    return ea


def ret_conversion(ret: Return) -> str:
    if isinstance(ret.return_type, VType):
        if ret.return_type.maybe_none:
            return "None if row[0] is None else %s(row[0])" % ret.return_type.name
        else:
            return "%s(row[0])" % ret.return_type.name
    elif isinstance(ret.return_type, RowType):
        return "%s(*row)" % ret.return_type.name
    else:
        raise TypeError("Uexpected type: %r" % ret.return_type)


def fn_return(ret: Optional[Return]) -> str:
    if ret is None:
        return "None"

    if ret.returns_one:
        if isinstance(ret.return_type, VType):
            return "Optional[%s]" % ret.return_type.name
        elif isinstance(ret.return_type, RowType):
            return "Optional[%s]" % ret.return_type.name
        else:
            raise TypeError("Uexpected type: %r" % ret.return_type)
    else:
        if isinstance(ret.return_type, VType):
            return "Iterable[%s]" % py_type(ret.return_type)
        elif isinstance(ret.return_type, RowType):
            return f"Iterable[%s]" % ret.return_type.name
        else:
            raise TypeError("Uexpected type: %r" % ret.return_type)


def generate(text: str, src: str, dbcon: str, typeguard: bool, verbose: bool) -> str:
    """Generate python from annotated sql."""
    parser = get_parser()
    transformer = SqlPyGenTransformer()
    env = Environment(
        loader=PackageLoader("sqlpygen", ""),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters.update(
        dict(
            py_type=py_type,
            fn_params=fn_params,
            query_args=query_args,
            explain_args=explain_args,
            fn_return=fn_return,
            ret_conversion=ret_conversion,
        )
    )

    if verbose:
        console = Console()

    try:
        parse_tree = parser.parse(text)
    except UnexpectedToken as e:
        line, col = e.line - 1, e.column - 1
        col_m1 = max(0, col)
        err_line = text.split("\n")[line]
        err_marker = "-" * col_m1 + "^"
        msg = f"Error parsing input:\n{e}\n{err_line}\n{err_marker}"
        raise RuntimeError(msg)

    if verbose:
        console.rule("Parse Tree")  # type: ignore
        console.print(parse_tree)  # type: ignore

    trans_tree = transformer.transform(parse_tree)

    if verbose:
        console.rule("Transformed tree")  # type: ignore
        console.print(trans_tree)  # type: ignore

    template = env.get_template("sqlpygen.jinja2")

    ctr = Counter(s.name for s in trans_tree.schemas)
    for name, n in ctr.most_common():
        if n > 1:
            raise RuntimeError("Schema %s is defined more than once." % name)

    ctr = Counter(s.name for s in trans_tree.queries)
    for name, n in ctr.most_common():
        if n > 1:
            raise RuntimeError("Query %s is defined more than once." % name)

    row_types = {}
    for query in trans_tree.queries:
        if query.return_ is not None and isinstance(query.return_.return_type, RowType):
            ret = query.return_.return_type
            if ret.name in row_types:
                if ret != row_types[ret.name]:
                    raise RuntimeError(
                        "Two row types of different kind have the same name: %s"
                        % ret.name
                    )
                continue
            row_types[ret.name] = ret

    rendered_tree = template.render(
        src=src,
        dbcon=dbcon,
        typeguard=typeguard,
        module=trans_tree.module,
        schemas=trans_tree.schemas,
        queries=trans_tree.queries,
        row_types=list(row_types.values()),
    )
    rendered_tree = format_str(rendered_tree, mode=Mode())
    return rendered_tree
