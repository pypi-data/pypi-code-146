import ast
import inspect
from types import FrameType
from typing import Any, Callable, Dict, Optional, Union

from executing import Source

from chalk.features import Filter


class ExecutingException(Exception):
    pass


class RetrievingError(ExecutingException):
    pass


def _get_node_by_frame(frame: FrameType, raise_exc: bool = True) -> Optional[ast.AST]:
    """Get the node by frame, raise errors if possible"""
    exect = Source.executing(frame)

    if exect.node:
        # attach the frame for better exception message
        # (i.e. where ImproperUseError happens)
        exect.node.__frame__ = frame  # type: ignore
        return exect.node

    assert isinstance(exect.source, Source)
    if exect.source.text and exect.source.tree and raise_exc:
        raise RetrievingError(
            (
                "Couldn't retrieve the call node. "
                "This may happen if you're using some other AST magic at the "
                "same time, such as pytest, ipython, macropy, or birdseye."
            )
        )

    return None


def _get_func_frame_and_nodes(condition: Callable[[Optional[ast.AST]], bool]):
    frames = inspect.stack()
    for frame_info in frames[3:]:
        frame = frame_info.frame
        func_node = _get_node_by_frame(frame)
        if condition(func_node):
            # This is the correct getitem frame.
            # It is important that the "slice" isn't an ast.Name,
            # as otherwise it would be impossible to parse the expression
            # ast.Name would imply something like this:
            # def __getitem__(self, item):
            #    return self.df[item]  # <--- item is of type ast.name. We need to go one frame higher!
            return frame, func_node
    raise RuntimeError("Condition not found in stack")


def parse_dataframe_getitem():
    func_frame, func_node = _get_func_frame_and_nodes(
        lambda node: isinstance(node, ast.Subscript) and not isinstance(node.slice, ast.Name)
    )
    assert isinstance(func_node, ast.Subscript)
    slc = func_node.slice
    if isinstance(slc, ast.Index):
        slc = slc.value  # type: ignore
        assert isinstance(slc, ast.expr)
    converted_slice = convert_slice(slc)
    return eval_converted_expr(converted_slice, glbs=func_frame.f_globals, lcls=func_frame.f_locals)


def parse_when() -> Optional[Filter]:
    func_frame, func_node = _get_func_frame_and_nodes(lambda node: isinstance(node, ast.Call))
    assert isinstance(func_node, ast.Call)
    when = next((k for k in func_node.keywords if k.arg == "when"), None)
    when_filter = convert_slice(when.value) if when else None
    assert isinstance(when_filter, ast.expr)
    return (
        eval_converted_expr(when_filter, glbs=func_frame.f_globals, lcls=func_frame.f_locals) if when_filter else None
    )


def _convert_maybe_tuple(slc: ast.expr):
    if isinstance(slc, ast.Tuple):
        return ast.Tuple(
            elts=[_convert_ops(x) for x in slc.elts],
            ctx=slc.ctx,
        )
    else:
        assert isinstance(slc, ast.expr)
        return _convert_ops(slc)


def convert_slice(slc: Union[ast.expr, ast.Index]):
    if isinstance(slc, ast.Index):
        # Index is deprecated in Python 3.9+
        slc = slc.value  # type: ignore
        assert isinstance(slc, ast.expr)
        slc = _convert_maybe_tuple(slc)
        return ast.Index(value=slc)
    return _convert_maybe_tuple(slc)


def eval_converted_expr(expr: ast.AST, glbs: Optional[Dict[str, Any]] = None, lcls: Optional[Dict[str, Any]] = None):
    expr.lineno = 1
    expr.col_offset = 0
    expr.end_lineno = 1
    expr.end_col_offset = 0
    expression = ast.Expression(body=expr)
    ast.fix_missing_locations(expression)
    glbs = dict(glbs or {})  # shallow copy
    # Inject the __CHALK_FILTER__ so the converted "in" and "not in" expressions can be parsed
    glbs["__CHALK_FILTER__"] = Filter
    return eval(compile(expression, filename="<string>", mode="eval"), glbs, lcls)  # nosemgrep: eval-detected


def _convert_ops(stmt: ast.expr):
    """Recursively convert operations so that they can be parsed by the filters"""
    if isinstance(stmt, ast.BoolOp):
        assert len(stmt.values) >= 2, "bool ops need at least two values"
        op: ast.operator
        if isinstance(stmt.op, ast.And):
            op = ast.BitAnd()
        elif isinstance(stmt.op, ast.Or):
            op = ast.BitOr()
        else:
            raise ValueError(f"Invalid op: {stmt.op}")
        values = list(stmt.values)
        ans = _convert_ops(values.pop())
        while len(values) > 0:
            left = values.pop()
            ans = ast.BinOp(
                left=_convert_ops(left),
                op=op,
                right=ans,
            )
        return ans
    if isinstance(stmt, ast.UnaryOp):
        if isinstance(stmt.op, ast.Not):
            return ast.UnaryOp(
                op=ast.Invert(),
                operand=_convert_ops(stmt.operand),
            )
        return stmt
    if isinstance(stmt, ast.Compare):
        if len(stmt.ops) == 1:
            lhs = stmt.left
            assert len(stmt.comparators) == 1
            rhs = stmt.comparators[0]
            compare_op: ast.cmpop = stmt.ops[0]
            # Replace is with == and isnot with !=
            # It doesn't make sense to have identity checks in a dataframe filter

            if isinstance(compare_op, ast.Is):
                return ast.Compare(left=lhs, ops=[ast.Eq()], comparators=[rhs])
            if isinstance(compare_op, ast.IsNot):
                return ast.Compare(left=lhs, ops=[ast.NotEq()], comparators=[rhs])

            if isinstance(compare_op, (ast.In, ast.NotIn)):
                filter_op = "in" if isinstance(compare_op, ast.In) else "not in"
                return ast.Call(
                    func=ast.Name(id="__CHALK_FILTER__", ctx=ast.Load()),
                    args=[
                        stmt.left,
                        ast.Constant(value=filter_op),
                        rhs,
                    ],
                    keywords=[],
                )
        return stmt
    return stmt
