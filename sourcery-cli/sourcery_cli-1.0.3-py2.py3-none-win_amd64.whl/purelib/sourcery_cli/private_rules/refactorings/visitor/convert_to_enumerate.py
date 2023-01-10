from typing import Optional, Set
from typing import Tuple as Tpl
from typing import Type

from sourcery.analysis.variable_usage import possible_assignments
from sourcery.ast import (
    AST,
    Assign,
    AugAssign,
    BinOp,
    Call,
    Constant,
    Expression,
    For,
    Keyword,
    Name,
    Node,
    Statement,
    Tuple,
    previous_sibling_assign,
)
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import ENUMERATE_DESC
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    LocalValueChanged,
    LocalValueMissing,
    SemanticDifference,
)


class ConvertToEnumerateProposer(
    Proposer, DependencyConditions, VariableUsageConditions
):
    """AST walker that proposes using enumerate in for loops."""

    def enter_for(self, node: For):
        if (
            node.is_async
            or node.orelse
            or len(node.body) <= 1
            or self.is_enumerate(node.iter)
        ):
            return

        increment, reads_after = self.find_increment(node)
        if increment and isinstance(increment.target, Name):
            increment_var = increment.target.unparse()
            prev_assign = previous_sibling_assign(node, increment_var)
            if (
                prev_assign
                and self.valid_prev_assign(prev_assign, increment.target)
                and not self.is_accessed_later(increment.target, node)
                and not self.writes_any_variables(node.target, increment.target)
            ):
                start_value = prev_assign.value.value  # type: ignore

                if reads_after:
                    start_value += 1

                self.propose(
                    ConvertToEnumerateProposal(
                        self.ast, node, increment, prev_assign, start_value
                    )
                )

    def valid_prev_assign(self, prev_assign: Assign, target: Name):
        return (
            isinstance(prev_assign.value, Constant)
            and prev_assign.value.type == int
            and hash(prev_assign.targets[0]) == hash(target)
        )

    def is_enumerate(self, node_iter: Node):
        return isinstance(node_iter, Call) and node_iter.func.unparse() == "enumerate"

    # TODO merge this with the while code.
    def find_increment(self, node: For) -> Tpl[Optional[AugAssign], bool]:
        """Returns an augassign if there is one and whether there are reads after it."""
        for index, statement_node in enumerate(node.body):
            if self.is_increment(statement_node):
                assert isinstance(statement_node, AugAssign)

                if any(
                    not self.passes_dep_check(node, statement_node.target)
                    for node in node.body[:index] + node.body[index + 1 :]
                ):
                    break

                reads_before = self.reads_any_variables(
                    node.body[:index], statement_node.target
                )
                reads_after = self.reads_any_variables(
                    node.body[index + 1 :], statement_node.target
                )

                if reads_before and reads_after:
                    break

                return statement_node, reads_after
        return None, False

    def passes_dep_check(self, node: Statement, variable: Node) -> bool:
        # Loop anchors might cause the while to skip the increment
        return not (
            self.is_loop_anchor(node)
            or variable.unparse() in possible_assignments(self.variable_usage[node])
        )

    def is_increment(self, node_statement: Statement) -> bool:
        return (
            isinstance(node_statement, AugAssign)
            and node_statement.op == BinOp.ADD
            and isinstance(node_statement.value, Constant)
            and node_statement.value.value == 1
        )


class ConvertToEnumerateProposal(Proposal):
    """Convert manual loop counter into call to enumerate."""

    def __init__(
        self, ast: AST, node: For, increment: AugAssign, prev_assign: Assign, start: int
    ) -> None:
        self.ast = ast
        self.node = node
        self.increment = increment
        self.previous_assign = prev_assign
        self.start = start
        self.node_index = self.node.parent.index(self.node)

    def description(self):
        return ENUMERATE_DESC

    def execute(self) -> None:
        if isinstance(self.node.target, Tuple):
            self.node.target.clear_original_source()

        self.node.iter = self.create_enumerate(self.node.iter, self.start)
        self.node.target = Tuple(
            (
                Name(self.increment.target.unparse()),
                self.node.target,
            )
        )

        self.node.parent.remove(self.previous_assign)
        self.node.body.remove(self.increment)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {LocalValueMissing, LocalValueChanged, LocalChangeOnException}

    def create_enumerate(self, existing_iter: Expression, start: int):
        name = Name("enumerate")
        keywords = (Keyword(Name("start"), Constant(start)),) if start else ()
        return Call(name, (existing_iter, *keywords))
