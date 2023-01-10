from math import copysign
from typing import List, Set, Type, Union

from sourcery.analysis.node_dependencies import (
    Dependencies,
    NodeDependencies,
    dependency_conflict,
    non_block_read_writes,
)
from sourcery.analysis.variable_usage import VariableUsage, possible_assignments
from sourcery.ast import AST, Assign, Call, Constant, Expression, For
from sourcery.ast import List as Lst
from sourcery.ast import Set as St
from sourcery.ast import Statement
from sourcery.ast import Tuple as Tpl
from sourcery.ast import While
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import HOIST_FOR_WHILE_BODY_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionRemoved,
    ExceptionTypeChanged,
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)

Loop = Union[For, While]


class HoistStatementFromLoopProposer(Proposer, DependencyConditions, LiteralConditions):
    """AST walker that proposes improvements to for loops."""

    node_dependencies: NodeDependencies
    variable_usage: VariableUsage

    def enter_for(self, node: For):
        if node.is_async:
            return
        if statements := self.hoistable_statements(node):
            self.propose(HoistStatementFromLoopProposal(self.ast, node, statements))

    def enter_while(self, node: While):
        if statements := self.hoistable_statements(node):
            self.propose(HoistStatementFromLoopProposal(self.ast, node, statements))

    def hoistable_statements(self, node: Loop) -> List[Statement]:
        return [
            statement
            for index, statement in enumerate(node.body)
            if self.can_hoist_statement(node, statement, index)
        ]

    def can_hoist_statement(self, node: Loop, statement: Statement, index: int):
        # pylint: disable=too-many-return-statements

        # Limit to assignments to prevent problems hoisting nested
        # augassigns. Also prevents hoisting strings and things
        # with breaks/continues
        if not isinstance(statement, Assign):
            return False

        if self.writes_any_variables(statement.value):
            return False

        statement_deps = self.node_dependencies[statement]
        node_reads, node_writes = non_block_read_writes(node, self.node_dependencies)

        if not self.only_assignment_writes(statement_deps):
            return False

        # Can hoist if the variables written are not read afterwards or
        # the loop is guaranteed to execute at least once
        elif not (
            self.loop_will_execute(node) or self.no_reads_after_loop(statement_deps)
        ):
            return False

        # can't hoist it past the loop counter
        elif dependency_conflict(statement_deps, node_reads, node_writes):
            return False

        elif self.statement_dep_conflict(node, statement_deps, index):
            return False
        else:
            return True

    def loop_will_execute(self, loop: Loop) -> bool:
        if isinstance(loop, While):
            return isinstance(loop.test, Constant) and loop.test.value
        else:
            return self.is_non_empty_collection(loop.iter) or self.is_valid_range_call(
                loop.iter
            )

    def is_non_empty_collection(self, node: Expression):
        return isinstance(node, (Tpl, Lst, St)) and node.elts

    def is_valid_range_call(self, node: Expression):
        if (
            isinstance(node, Call)
            and node.func.unparse() == "range"
            and all(self.is_numeric_literal(arg) for arg in node.args)
        ):
            if len(node.args) == 1:
                if node.args[0].unparse() != "0":
                    return True
            elif len(node.args) == 2:
                if node.args[0].value < node.args[1].value:  # type: ignore
                    return True
            elif len(node.args) == 3:
                if node.args[0].value < node.args[1].value * copysign(  # type: ignore
                    1, node.args[2].value  # type: ignore
                ):
                    return True
        return False

    def no_reads_after_loop(self, statement_deps: Dependencies):
        return all(
            edge.to_.node != statement_deps.node.parent
            for edge in statement_deps.outgoing.values()
        )

    def only_assignment_writes(self, statement_deps: Dependencies):
        # Only allow statements which don't write or assign something and
        # don't read it as well.

        var_assignments = possible_assignments(self.variable_usage[statement_deps.node])

        return not statement_deps.reads_vars(var_assignments)

    def statement_dep_conflict(
        self, node: Loop, statement_deps: Dependencies, statement_index: int
    ):
        reads_and_writes = statement_deps.all_reads_and_writes()

        for other_index, other_statement in enumerate(node.body.statements):
            if other_index == statement_index:
                continue

            other_dep = self.node_dependencies[other_statement]

            # check the statement can move past the earlier ones
            # N.B we can't move past break/continues
            if other_index < statement_index and (
                other_dep.is_loop_anchor
                or dependency_conflict(
                    statement_deps, set(other_dep.reads), other_dep.all_writes()
                )
            ):
                return True

            if other_dep.writes_vars(reads_and_writes):
                return True

        return False


class HoistStatementFromLoopProposal(Proposal):
    """Hoists statements out of a for statement to execute them only once."""

    def __init__(self, ast: AST, node: Loop, statements: List[Statement]) -> None:
        self.ast = ast
        self.node = node
        self.statements = statements

    def description(self):
        return HOIST_FOR_WHILE_BODY_DESC

    def execute(self) -> None:
        for_index = self.node.parent.index(self.node)
        for statement in reversed(self.statements):
            self.node.body.remove(statement)
            self.node.parent.insert(for_index, statement)
        if not self.node.body and isinstance(self.node, For):
            self.node.parent.remove(self.node)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {
            LocalValueMissing,
            LocalChangeOnException,
            ExceptionTypeChanged,
            ExceptionRemoved,
        }
