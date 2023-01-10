import ast
from typing import Any, List, Set, Tuple, Union, cast

import networkx as nx
from typing_extensions import get_args

from classiq.interface.generator.arith.ast_node_rewrite import AstNodeRewrite

from classiq.exceptions import ClassiqArithmeticError

_REPEATED_VARIABLES_ERROR_MESSAGE: str = (
    "Repeated variables in the beginning of an arithmetic expression are not allowed."
)
_ILLEGAL_PARSED_GRAPH_ERROR_MESSAGE: str = "parsed graph contains multiple result nodes"
_ALLOWED_MULTI_ARGUMENT_FUNCTIONS = ("min", "max")

SUPPORTED_FUNC_NAMES: Set[str] = {"CLShift", "CRShift", "min", "max"}

SupportedNodesTypes = Union[
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
    ast.Invert,
    ast.Compare,
    ast.Eq,
    ast.Mod,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.USub,
    ast.UAdd,
    ast.Sub,
    ast.Gt,
    ast.GtE,
    ast.Lt,
    ast.LtE,
    ast.NotEq,
    ast.LShift,
    ast.RShift,
    ast.Call,
    ast.Mult,
]


class ExpressionVisitor(ast.NodeVisitor):
    def __init__(self, supported_nodes) -> None:
        super().__init__()
        self.graph = nx.DiGraph()
        self.supported_nodes = get_args(supported_nodes)

    @staticmethod
    def _check_repeated_variables(variables: Tuple[Any, Any]) -> None:
        if (
            all(isinstance(var, ast.Name) for var in variables)
            and variables[0].id == variables[1].id
        ):
            raise ClassiqArithmeticError(_REPEATED_VARIABLES_ERROR_MESSAGE)

    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, self.supported_nodes):
            return ast.NodeVisitor.generic_visit(self, node)
        raise ClassiqArithmeticError(
            f"{type(node).__name__} is not suitable for arithmetic expression"
        )

    def visit_Compare(self, node: ast.Compare) -> None:
        self._check_repeated_variables((node.left, node.comparators[0]))
        self.update_graph(
            node,
            cast(SupportedNodesTypes, node.left),
            cast(SupportedNodesTypes, node.comparators[0]),
        )
        self.generic_visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        self._check_repeated_variables((node.left, node.right))
        self.update_graph(
            node,
            cast(SupportedNodesTypes, node.left),
            cast(SupportedNodesTypes, node.right),
        )
        self.generic_visit(node)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        self.update_graph(node, cast(SupportedNodesTypes, node.operand))
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if len(node.args) >= 2:
            self._check_repeated_variables((node.args[0], node.args[1]))
        node_id = AstNodeRewrite().extract_node_id(node)
        if node_id not in SUPPORTED_FUNC_NAMES:
            raise ClassiqArithmeticError(f"{node_id} not in supported functions")

        if node_id in ("CLShift", "CRShift") and (
            len(node.args) != 2 or not isinstance(node.args[1], ast.Constant)
        ):
            raise ClassiqArithmeticError("Cyclic Shift expects 2 arguments (exp, int)")

        self.update_graph(node, *cast(List[SupportedNodesTypes], node.args))
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> None:
        if not isinstance(node.value, (int, float)):
            raise ClassiqArithmeticError(
                f"{type(node.value).__name__} literals are not valid in arithmetic expressions"
            )
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.update_graph(node, *cast(List[SupportedNodesTypes], node.values))
        self.generic_visit(node)

    def update_graph(
        self, child_node: SupportedNodesTypes, *parent_nodes: SupportedNodesTypes
    ) -> None:
        child_node_id = AstNodeRewrite().extract_node_id(child_node)

        for parent_node in parent_nodes:
            parent_node_id = AstNodeRewrite().extract_node_id(parent_node)
            self.graph.add_edge(parent_node_id, child_node_id)

        mod_output_size = getattr(child_node, "output_size", None)
        if mod_output_size:
            self.graph.nodes[child_node_id]["output_size"] = mod_output_size

            for node in parent_nodes:
                nod_output_size = getattr(node, "output_size", mod_output_size)

                new_output_size = min(mod_output_size, nod_output_size)
                node.output_size = new_output_size  # type: ignore[union-attr]

                node_id = AstNodeRewrite().extract_node_id(node)
                self.graph.nodes[node_id]["output_size"] = new_output_size


class InDegreeLimiter:
    @staticmethod
    def _condition(graph: nx.DiGraph, node: str) -> bool:
        return graph.in_degree[node] > 2 and node in _ALLOWED_MULTI_ARGUMENT_FUNCTIONS

    @staticmethod
    def _node_conversion(graph: nx.DiGraph, node: str) -> nx.DiGraph:
        relevant_in_edges = graph.in_edges(node)
        last_node_added = node
        for idx, in_edge in enumerate(list(relevant_in_edges)[2:]):
            graph.remove_edge(*in_edge)
            new_node = node + f"_copy_{idx}"
            graph.add_node(new_node)
            for out_edge in list(graph.out_edges(last_node_added)):
                graph.add_edge(new_node, out_edge[1])
                graph.remove_edge(*out_edge)
            graph.add_edge(last_node_added, new_node)
            graph.add_edge(in_edge[0], new_node)
            last_node_added = new_node
        return graph

    @classmethod
    def graph_conversion(cls, graph: nx.DiGraph) -> nx.DiGraph:
        for node in list(graph.nodes):
            if cls._condition(graph, node):
                graph = cls._node_conversion(graph, node)
        if num_of_result_nodes(graph) != 1:
            raise ClassiqArithmeticError(_ILLEGAL_PARSED_GRAPH_ERROR_MESSAGE)
        return graph


def parse_expression(
    expression: str,
    *,
    validate_degrees: bool,
    supported_nodes=SupportedNodesTypes,
) -> nx.DiGraph:
    ast_expr = ast.parse(expression, "", "eval")
    ast_obj = AstNodeRewrite().visit(ast_expr)
    visitor = ExpressionVisitor(supported_nodes)
    visitor.visit(ast_obj)
    if validate_degrees:
        return InDegreeLimiter.graph_conversion(graph=visitor.graph)
    return visitor.graph


def num_of_result_nodes(graph: nx.DiGraph) -> int:
    return sum(int(graph.out_degree(node) == 0) for node in graph.nodes)


def validate_expression(
    expression: str, *, validate_degrees: bool, supported_nodes=SupportedNodesTypes
) -> None:
    parse_expression(
        expression, validate_degrees=validate_degrees, supported_nodes=supported_nodes
    )
