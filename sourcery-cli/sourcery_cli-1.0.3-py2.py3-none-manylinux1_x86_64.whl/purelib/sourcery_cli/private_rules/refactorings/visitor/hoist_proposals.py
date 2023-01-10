"""Contains refactorings for code hoisting."""
from enum import Enum
import typing
from typing import List, NamedTuple, Optional, Set, Tuple, Type, Union

from sourcery.analysis.clone_detection import NodeClones
from sourcery.analysis.node_dependencies import (
    Edge,
    NodeDependencies,
    ReadWrite,
    VariableEdgeType,
    WriteRead,
)
from sourcery.ast import (
    AST,
    Assign,
    AugAssign,
    BinOp,
    Block,
    Compare,
    Constant,
    Elif,
    Expression,
    For,
    If,
    Node,
    Statement,
    While,
    is_single_block,
)
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import HOIST_DESC, HOIST_FOR_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionRemoved,
    ExceptionTypeChanged,
    LocalChangeOnException,
    ReturnValuesChangedOnException,
    SemanticDifference,
    StdOutChangedOnException,
)


class HoistDirection(Enum):
    UP = 0
    DOWN = 1


class OperatorChange(NamedTuple):
    nodes_to_change: List[Expression]
    operator: BinOp.Op
    change_by: Expression


class AssignChange(NamedTuple):
    nodes_to_change: List[Expression]
    value: Expression


Change = Union[OperatorChange, AssignChange]


class HoistStatementFromIfProposer(MultiProposer, DependencyConditions):
    """AST walker that proposes the code hoisting refactoring.

    Finds identical blocks of code inside
    each branch of an if..elif..else conditional.
    Needs to check that either there are no
    internal dependencies in the conditional, or that
    these are always before or after not both.
    If the dependencies are simple compares and the statement
    to move is AugAssign it will alter the compares.
    """

    node_dependencies: NodeDependencies
    node_clones: NodeClones
    blocks_stack: List[List[Block]]

    AUGASSIGN_OPS = {BinOp.ADD, BinOp.SUB, BinOp.MULT, BinOp.DIV}

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {HoistStatementFromIfProposal, HoistLoopFromIfProposal}

    def reset(self, ast):
        super().reset(ast)
        self.blocks_stack: List[List[Block]] = []

    def enter_if(self, node: If):
        self.blocks_stack.append([node.body])

    def enter_elif(self, node: Elif):
        self.blocks_stack[-1].append(node.body)

    def enter_block(self, node: Block):
        if isinstance(node.parent, If) and node.is_else_block():
            self.blocks_stack[-1].append(node)

    def leave_if(self, node: If):
        current_blocks = self.blocks_stack.pop()

        if self._reached_valid_else(node, current_blocks):
            for potential_hoist in current_blocks[0]:
                self._propose_hoist(node, current_blocks, potential_hoist)

        if len(current_blocks) > 1 and self._valid_for_while(node, current_blocks):
            assert isinstance(current_blocks[0].parent, If)
            self.propose(
                HoistLoopFromIfProposal(
                    self.ast, current_blocks, current_blocks[0].parent
                )
            )

    def _valid_for_while(self, node: If, blocks: List[Block]):
        return self._all_blocks_valid(node, blocks) and not self._dependency_conflict(
            blocks
        )

    def _all_blocks_valid(self, node: If, blocks: List[Block]):
        if all(
            self._is_valid_block(block, For) and not block[0].is_async
            for block in blocks
        ):
            hash_value = self._for_hash(blocks[0][0])
            return all(self._for_hash(block[0]) == hash_value for block in blocks)

        if node.orelse and all(self._is_valid_block(block, While) for block in blocks):
            hash_value = hash(blocks[0][0].test)
            return all(hash(block[0].test) == hash_value for block in blocks)

        return False

    def _dependency_conflict(self, blocks: List[Block]):  # sourcery skip
        tests = [block.parent for block in blocks]
        for block in blocks:
            if not all(self.can_be_moved_past(block, test) for test in tests):
                return True
        return False

    def _is_valid_block(self, block: Block, type_to_check: type):
        return is_single_block(block, type_to_check) and not block[0].orelse

    def _for_hash(self, for_node: For):
        return hash((for_node.iter, for_node.target))

    # Don't want to completely remove a conditional with side effects in its test
    def _reached_valid_else(self, node: If, current_blocks: List[Block]):
        return current_blocks[-1].is_else_block() and not (
            self.writes_any_variables(node.test) and len(current_blocks[0]) == 1
        )

    def _propose_hoist(
        self, node: If, current_blocks: List[Block], potential_hoist: Statement
    ):
        clones_in_each_block = [
            [
                statement
                for statement in block
                if statement in self.node_clones[potential_hoist]
            ]
            for block in current_blocks
        ]

        if all(clones_in_each_block):
            clones_to_hoist = [potential_hoist] + [
                clones[0] for clones in clones_in_each_block[1:]
            ]
            hoist_direction, changes = self._hoist_direction(
                clones_to_hoist, current_blocks, node
            )
            if hoist_direction:
                self.propose(
                    HoistStatementFromIfProposal(
                        self.ast, node, clones_to_hoist, hoist_direction, changes
                    )
                )

    def _hoist_direction(
        self, block_clones: List[Statement], blocks: List[Block], if_node: If
    ) -> Tuple[(Optional[HoistDirection], List[Change])]:
        all_previous_changes = []
        all_following_changes = []

        possible_hoist_directions = {HoistDirection.DOWN, HoistDirection.UP}

        for block, node in zip(blocks, block_clones):
            index = block.index(node)

            # Check dependencies between the conditional and the hoist
            if not self.can_be_moved_past(if_node, node):
                possible_hoist_directions.discard(HoistDirection.UP)

            dep = self.node_dependencies[node]

            previous_sibling_edges = {
                edge
                for dependency, edge in dep.incoming.items()
                if dependency.node in block[:index]
            }

            following_sibling_edges = {
                edge
                for dependency, edge in dep.outgoing.items()
                if dependency.node in block[index + 1 :]
            }

            previous_changes, following_changes = self._get_possible_changes(
                node, previous_sibling_edges, following_sibling_edges
            )

            if previous_sibling_edges and len(previous_changes) < len(
                previous_sibling_edges
            ):
                possible_hoist_directions.discard(HoistDirection.UP)

            if following_sibling_edges and len(following_changes) < len(
                following_sibling_edges
            ):
                possible_hoist_directions.discard(HoistDirection.DOWN)

            all_previous_changes.extend(previous_changes)
            all_following_changes.extend(following_changes)

        if HoistDirection.DOWN in possible_hoist_directions:
            return HoistDirection.DOWN, all_following_changes
        elif HoistDirection.UP in possible_hoist_directions:
            return HoistDirection.UP, all_previous_changes
        else:
            return None, []

    def _get_possible_changes(
        self,
        node_to_hoist: Node,
        previous_sibling_edges: Set[Edge],
        following_sibling_edges: Set[Edge],
    ) -> Tuple[List[Change], List[Change]]:
        previous_changes = self._get_changes(
            previous_sibling_edges, ReadWrite, node_to_hoist
        )
        following_changes = self._get_changes(
            following_sibling_edges, WriteRead, node_to_hoist
        )

        return previous_changes, following_changes

    def _get_changes(
        self, sibling_edges: Set[Edge], variable_edge_type, node_to_hoist: Node
    ) -> List[Change]:
        result: List[Change] = []

        # Assigns can only be moved downwards
        if (
            isinstance(node_to_hoist, AugAssign)
            and node_to_hoist.op in self.AUGASSIGN_OPS
        ) or (
            variable_edge_type == WriteRead
            and isinstance(node_to_hoist, Assign)
            and len(node_to_hoist.targets) == 1
        ):
            if isinstance(node_to_hoist, AugAssign):
                left_variable = node_to_hoist.target.unparse()
            else:
                left_variable = node_to_hoist.targets[0].unparse()

            # Look for simple edges which lead to Compare nodes
            valid_edge_type = {variable_edge_type(left_variable, left_variable, [], [])}
            for edge in sibling_edges:
                if edge.edge_types == valid_edge_type:
                    (edge_type,) = edge.edge_types
                    assert isinstance(edge_type, VariableEdgeType)
                    if change_nodes := self._get_nodes_to_change(
                        edge_type, node_to_hoist
                    ):
                        if isinstance(node_to_hoist, AugAssign):
                            result.append(
                                OperatorChange(
                                    change_nodes, node_to_hoist.op, node_to_hoist.value
                                )
                            )
                        else:
                            assert isinstance(node_to_hoist, Assign)
                            result.append(
                                AssignChange(change_nodes, node_to_hoist.value)
                            )
        return result

    def _get_nodes_to_change(
        self, edge_type: VariableEdgeType, node_to_hoist: Node
    ) -> List[Expression]:
        if isinstance(edge_type, ReadWrite):
            read_deps = edge_type.from_deps
        else:
            read_deps = edge_type.to_deps

        if all(self._node_can_be_changed(dep.node) for dep in read_deps):
            if isinstance(node_to_hoist, AugAssign):
                return [
                    dep.node.parent.comparators[0] for dep in read_deps  # type: ignore
                ]
            else:
                return [dep.node for dep in read_deps]  # type: ignore
        return []

    def _node_can_be_changed(self, node: Node):
        return isinstance(node.parent, Compare) and node.parent.left == node


class HoistStatementFromIfProposal(Proposal):
    """Hoists code that is always executed out of an if statement."""

    def __init__(
        self,
        ast: AST,
        node: If,
        statements_to_hoist: List[Statement],
        hoist_direction: HoistDirection,
        changes: List[Change],
    ) -> None:
        self.ast = ast
        self.node = node
        self.statements_to_hoist = statements_to_hoist
        self.blocks_processed: List[Tuple[Block, int]] = []
        self.hoist_direction = hoist_direction
        self.changes = changes

    def description(self):
        return HOIST_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return tuple(self.statements_to_hoist)

    def execute(self) -> None:
        self.remove_hoisted_statements()

        if_index = self.node.parent.index(self.node)
        if self.hoist_direction == HoistDirection.DOWN:
            self.node.parent.insert(if_index + 1, self.statements_to_hoist[0])
            apply_changes(self.changes, invert=True)
        else:
            assert self.hoist_direction == HoistDirection.UP
            self.node.parent.insert(if_index, self.statements_to_hoist[0])
            apply_changes(self.changes, invert=False)

        if not self.node.body and not self.node.elifs and not self.node.orelse:
            self.node.parent.remove(self.node)

    def remove_hoisted_statements(self) -> None:
        for statement in self.statements_to_hoist:
            parent = statement.parent

            assert isinstance(parent, Block)

            index = parent.index(statement)
            self.blocks_processed.append((parent, index))
            parent.remove(statement)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {
            LocalChangeOnException,
            ExceptionRemoved,
            ReturnValuesChangedOnException,
            ExceptionArgsChanged,
            ExceptionTypeChanged,
            StdOutChangedOnException,
        }


def apply_changes(changes, invert: bool):
    # pylint: disable=unidiomatic-typecheck

    results = []
    for change in changes:
        if isinstance(change, OperatorChange):
            oper = change.operator.invert() if invert else change.operator
            change_by_numeric = LiteralConditions().is_numeric_literal(change.change_by)

            for node in change.nodes_to_change:
                if change_by_numeric and LiteralConditions().is_numeric_literal(node):
                    assert isinstance(node, Constant)
                    assert isinstance(change.change_by, Constant)
                    new_value = oper(node.value, change.change_by.value)
                    if int(new_value) == new_value:
                        new_value = int(new_value)
                    if type(new_value) == type(node.value):
                        replacement: Expression = Constant(new_value)
                    else:
                        replacement = BinOp(
                            node.copy_as_root(),
                            oper,
                            change.change_by.copy_as_root(),
                        )
                else:
                    replacement = BinOp(
                        node.copy_as_root(),
                        oper,
                        change.change_by.copy_as_root(),
                    )

                results.append((node, node.replace(replacement)))
        else:
            assert isinstance(change, AssignChange)
            results.extend(
                (node, node.replace(change.value)) for node in change.nodes_to_change
            )

    return results


class HoistLoopFromIfProposal(Proposal):
    def __init__(self, ast: AST, blocks: List[Block], top_level_node: If) -> None:
        self.ast = ast
        self.blocks = blocks
        self.top_level_node = top_level_node

    def description(self):
        return HOIST_FOR_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return (self.top_level_node,)

    def execute(self) -> None:
        for_while = self.blocks[0][0]
        for block in self.blocks:
            block.statements = block[0].body.statements
            for statement in block:
                statement.parent = block

        if isinstance(for_while, For):
            replacement: Node = For(
                target=for_while.target,
                iter=for_while.iter,
                body=Block((self.top_level_node.copy_as_root(),)),
                orelse=Block(()),
            )
        else:
            replacement = While(
                test=for_while.test,
                body=Block((self.top_level_node.copy_as_root(),)),
                orelse=Block(()),
            )

        self.top_level_node.replace(replacement)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ExceptionRemoved, ReturnValuesChangedOnException}
