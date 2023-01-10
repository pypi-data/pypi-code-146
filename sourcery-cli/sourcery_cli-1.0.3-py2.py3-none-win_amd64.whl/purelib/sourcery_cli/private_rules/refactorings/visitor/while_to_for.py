from typing import Optional, Set, Tuple, Type

from sourcery.analysis.control_flow_next_node import ControlFlowNextNode
from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.analysis.nodes_in_loops import NodesInLoops
from sourcery.analysis.variable_usage import VariableUsage, accessed_later
from sourcery.ast import (
    AST,
    Assign,
    AugAssign,
    BinOp,
    Call,
    Compare,
    Constant,
    Expression,
    For,
    Name,
    Node,
    Statement,
    While,
    previous_sibling_assign,
)
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import WHILE_TO_FOR_DESC
from sourcery.rules.private.refactorings.visitor.hoist_proposals import (
    OperatorChange,
    apply_changes,
)
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    LocalChangeOnException,
    LocalValueChanged,
    LocalValueMissing,
    SemanticDifference,
)


class WhileToForProposer(Proposer, TypeConditions, LiteralConditions):
    """AST walker that proposes improvements to while loops."""

    node_dependencies: NodeDependencies
    var_usage: VariableUsage
    next_nodes: ControlFlowNextNode
    nodes_in_loops: NodesInLoops

    def enter_while(self, node: While):
        if len(node.body) <= 1 or node.orelse or not self.is_inequality(node.test):
            return
        assert isinstance(node.test, Compare)

        if not self.has_int_type(node.test.comparators[0]):
            return

        # If the comparator gets modified in the body we can't do this.
        comparator_vars = self.node_dependencies[
            node.test.comparators[0]
        ].all_reads_and_writes()

        if self.node_dependencies[node.body].writes_vars(comparator_vars):
            return

        left = node.test.left
        # We will remove this variable so it needs to be a simple Name
        if isinstance(left, Name):
            left_value = left.unparse()
            prev_assign = previous_sibling_assign(node, left_value)
            if (
                prev_assign
                and hash(prev_assign.targets[0]) == hash(left)
                and self.is_int_literal(prev_assign.value)
                and not accessed_later(
                    {left_value},
                    node,
                    self.var_usage,
                    self.next_nodes,
                    self.nodes_in_loops,
                )
            ):
                count_increment, reads_after = self.find_increment(node, left)
                if count_increment:
                    assert isinstance(count_increment.value, Constant)
                    if self.is_add(count_increment.op, count_increment.value.value):
                        increment = abs(count_increment.value.value)
                    else:
                        increment = -abs(count_increment.value.value)
                    self.propose(
                        WhileToForProposal(
                            self.ast,
                            node,
                            increment,
                            prev_assign,
                            count_increment,
                            reads_after,
                        )
                    )

    def is_inequality(self, node: Node):
        return (
            isinstance(node, Compare)
            and len(node.ops) == 1
            and node.ops[0] in (Compare.LT, Compare.LTE, Compare.GTE, Compare.GT)
        )

    def find_increment(
        self, while_node: While, target: Node
    ) -> Tuple[Optional[AugAssign], bool]:
        """Returns an augassign if there is one and whether there are reads after it."""
        assert isinstance(while_node.test, Compare)
        variable = target.unparse()
        while_op = while_node.test.ops[0]
        for index, statement_node in enumerate(while_node.body):
            if self.is_increment(statement_node, target, while_op):
                if any(
                    not self.passes_dep_check(node, variable)
                    for node in while_node.body[:index] + while_node.body[index + 1 :]
                ):
                    break
                reads_before = any(
                    self.node_dependencies[node].reads_vars([variable])
                    for node in while_node.body[:index]
                )
                reads_after = any(
                    self.node_dependencies[node].reads_vars([variable])
                    for node in while_node.body[index + 1 :]
                )
                if reads_before and reads_after:
                    break
                return statement_node, reads_after
        return None, False

    def passes_dep_check(self, node: Statement, variable: str) -> bool:
        # Loop anchors might cause the while to skip the increment
        return not (
            self.node_dependencies[node].is_loop_anchor
            or self.node_dependencies[node].writes_vars([variable])
        )

    def is_increment(
        self, node_statement: Statement, target: Node, while_op: Compare.Op
    ) -> bool:
        return (
            isinstance(node_statement, AugAssign)
            and hash(node_statement.target) == hash(target)
            and isinstance(node_statement.value, Constant)
            and node_statement.value.type == int
            and self.matching_increment(
                node_statement.op, node_statement.value.value, while_op
            )
        )

    def matching_increment(
        self, op: BinOp.Op, value: int, while_op: Compare.Op
    ) -> bool:
        return (while_op in [Compare.LTE, Compare.LT] and self.is_add(op, value)) or (
            while_op in [Compare.GT, Compare.GTE] and self.is_minus(op, value)
        )

    def is_add(self, op: BinOp.Op, value: int) -> bool:
        return (op == BinOp.ADD and value > 0) or (op == BinOp.SUB and value < 0)

    def is_minus(self, op: BinOp.Op, value: int) -> bool:
        return (op == BinOp.ADD and value < 0) or (op == BinOp.SUB and value > 0)


class WhileToForProposal(Proposal):
    """Convert while loop with counter to for loop."""

    def __init__(
        self,
        ast: AST,
        node: While,
        increment: int,
        prev_assign: Assign,
        count_increment: AugAssign,
        reads_after: bool,
    ) -> None:
        assert isinstance(node.test, Compare)
        self.ast = ast
        self.node = node
        self.increment = increment
        self.iterator = node.test.comparators[0]
        self.previous_assign = prev_assign
        self.previous_assign_index = prev_assign.parent.index(prev_assign)
        self.op = node.test.ops[0]
        self.node_index = self.node.parent.index(self.node)
        self.count_increment = count_increment
        self.reads_after = reads_after

    def description(self):
        return WHILE_TO_FOR_DESC

    def execute(self) -> None:
        start = self.previous_assign.value
        assert isinstance(start, Constant)
        stop = self.iterator
        stop_change = 0
        if self.reads_after:
            start.value += self.increment
            stop_change += self.increment
        if self.op == Compare.LTE:
            stop_change += 1
        elif self.op == Compare.GTE:
            stop_change -= 1
        if stop_change != 0:
            op = BinOp.ADD if stop_change > 0 else BinOp.SUB
            stop = apply_changes(
                [OperatorChange([stop], op, Constant(abs(stop_change)))], False
            )[0][1]
        new_for_iter = self.create_range_call(start, stop, self.increment)
        self.node.body.remove(self.count_increment)
        new_for = For(
            self.previous_assign.targets[0],
            new_for_iter,
            self.node.body,
            self.node.orelse,
        )
        self.node.parent.remove(self.previous_assign)
        self.node.replace(new_for)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {
            LocalValueChanged,
            LocalValueMissing,
            LocalChangeOnException,
            ExceptionArgsChanged,
        }

    def create_range_call(self, start: Constant, stop: Expression, increment: int):
        args = (
            (start, stop, Constant(increment))
            if increment > 1 or increment <= -1
            else (start, stop)
            if start.value != 0
            else (stop,)
        )

        return Call(Name("range"), args)
