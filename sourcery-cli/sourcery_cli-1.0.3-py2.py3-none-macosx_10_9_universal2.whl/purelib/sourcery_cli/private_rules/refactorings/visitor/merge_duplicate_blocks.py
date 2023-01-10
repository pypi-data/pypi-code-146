"""Contains refactorings for if nodes."""
from typing import Dict, Iterable, Iterator, List, NamedTuple, Tuple

from lib.util import groupby
from sourcery.analysis.logic_solver import Condition
from sourcery.ast import AST, Block, BoolOp, Elif, Expression, If, Node, Pass
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.metrics.simple_metrics import NodeSizes


class ConditionedBlock(NamedTuple):
    conditions: List[Condition]
    block: Block


class BlockList(NamedTuple):
    top_level_if: If
    blocks: List[ConditionedBlock]


class MergeDuplicateBlocksProposer(Proposer, DependencyConditions):
    """AST walker that proposes merging if conditions with identical blocks."""

    block_stack: List[BlockList]
    conditions: Dict[Node, List[Condition]]
    node_sizes: NodeSizes

    MAX_BLOCKS = 5
    MAX_CONDITIONAL_SIZE = 8

    def reset(self, ast: AST):
        super().reset(ast)
        self.block_stack: List[BlockList] = []
        self.conditions: Dict[Node, List[Condition]] = {}

    def enter_block(self, node: Block):
        # Record conditions from on block from parent If and Elifs
        parent = node.parent
        if isinstance(parent, If):
            if parent.body == node:
                self.conditions[node] = [Condition(parent.test)]
            else:
                conditions = list(
                    self.conditions[parent.elifs[-1].body]
                    if parent.elifs
                    else self.conditions[parent.body]
                )
                conditions[-1] = Condition(conditions[-1].node, inverted=True)
                self.conditions[node] = conditions

        elif isinstance(parent, Elif):
            if_node = parent.parent
            if elif_index := if_node.elifs.index(parent):
                conditions = list(self.conditions[if_node.elifs[elif_index - 1].body])
                conditions[-1] = Condition(conditions[-1].node, inverted=True)
                conditions.append(Condition(parent.test))
                self.conditions[node] = conditions
            else:
                self.conditions[node] = [
                    Condition(if_node.test, inverted=True),
                    Condition(parent.test),
                ]

    def leave_if(self, node: If):
        working_blocks = []
        blocks_to_add = [node.body, *(elif_.body for elif_ in node.elifs), node.orelse]

        for block_list in self.block_stack:
            parent_block = block_list.top_level_if.parent
            if parent_block in blocks_to_add:
                # Merge parent_block and block_list
                for conditioned_block in block_list.blocks:
                    conditioned_block.conditions[:0] = self.conditions[parent_block]
                blocks_to_add.remove(parent_block)
                working_blocks.extend(block_list.blocks)

        working_blocks.extend(
            ConditionedBlock(self.conditions[block], block) for block in blocks_to_add
        )

        proposed = self.propose_reshape(working_blocks, node)

        self.block_stack = [
            block_list
            for block_list in self.block_stack
            if block_list.top_level_if.parent.parent != node
        ]
        if not proposed and self.part_of_if_chain(node):
            self.block_stack.append(BlockList(node, working_blocks))

    def propose_reshape(
        self, conditioned_blocks: List[ConditionedBlock], top_level_if: If
    ) -> bool:
        non_empty_conditioned = [cb for cb in conditioned_blocks if cb.block]

        if len(non_empty_conditioned) <= self.MAX_BLOCKS:
            grouped_blocks = list(
                groupby(conditioned_blocks, key=lambda cb: hash(cb.block)).values()
            )

            non_empty_groups = [g for g in grouped_blocks if g[0].block]

            if any(
                self.writes_any_variables(duplicate_nodes)
                for conditioned_blocks in grouped_blocks
                for duplicate_nodes in (
                    _get_node_duplicates_in_conditions(
                        _get_conditions_in_test_for_conditioned_blocks(
                            conditioned_blocks
                        )
                    )
                )
            ):
                # disallow duplicating nodes that have side-effects.
                # for instance, this refactoring would want to refactor
                #
                #     if cond1():
                #         if cond2:
                #             body()
                #     else:
                #         body()
                #
                # into
                #
                #     if cond1() and cond2 or not cond1():
                #         body()
                #
                # which is wrong since now `cond1()` would get called twice
                return False

            if (
                0 < len(non_empty_groups) < len(non_empty_conditioned)
                and self.max_conditional_size(non_empty_conditioned)
                < self.MAX_CONDITIONAL_SIZE
            ):
                self.propose(
                    MergeDuplicateBlocksProposal(self.ast, grouped_blocks, top_level_if)
                )
                return True

        return False

    def max_conditional_size(self, non_empty_conditioned) -> float:
        condition_lists = [
            conditioned_block.conditions for conditioned_block in non_empty_conditioned
        ]
        conditions = [item for sublist in condition_lists for item in sublist]
        return max(self.node_sizes[condition.original_node] for condition in conditions)

    def part_of_if_chain(self, node: If):
        return isinstance(node.parent.parent, (If, Elif)) and len(node.parent) == 1


class MergeDuplicateBlocksProposal(Proposal):
    """Proposal to merge duplicate blocks in conditionals."""

    def __init__(
        self,
        ast: AST,
        reconfigured_blocks: List[List[ConditionedBlock]],
        top_level_if: If,
    ) -> None:
        self.ast = ast
        self.top_level_if = top_level_if
        self.reconfigured_blocks = reconfigured_blocks

    def description(self):
        return "Merge duplicate blocks in conditional"

    def target_nodes(self) -> Tuple[If]:
        return (self.top_level_if,)

    def execute(self) -> None:
        if len(self.reconfigured_blocks) > 1:
            (
                if_conditioned_block,
                *elifs_conditioned_blocks,
                else_conditioned_blocks,
            ) = self.reconfigured_blocks
        else:
            if_conditioned_block = self.reconfigured_blocks[0]
            elifs_conditioned_blocks = []
            else_conditioned_blocks = []

        elifs = tuple(
            Elif(
                test=self.create_test(conditioned_blocks),
                body=conditioned_blocks[0].block or Block((Pass(),)),
            )
            for conditioned_blocks in elifs_conditioned_blocks
        )

        replacement_if = If(
            test=self.create_test(if_conditioned_block),
            body=if_conditioned_block[0].block,
            elifs=elifs,
            orelse=else_conditioned_blocks[0].block
            if else_conditioned_blocks
            else Block(()),
        )

        self.top_level_if.replace(replacement_if)

    def create_test(self, conditioned_blocks: List[ConditionedBlock]) -> Expression:
        if len(conditioned_blocks) > 1:
            return BoolOp(
                op=BoolOp.OR,
                values=tuple(
                    self.conditionals_to_node(block.conditions)
                    for block in conditioned_blocks
                ),
            )
        else:
            return self.conditionals_to_node(conditioned_blocks[0].conditions)

    def conditionals_to_node(self, conditions: List[Condition]) -> Expression:
        if len(conditions) > 1:
            return BoolOp(
                op=BoolOp.AND,
                values=tuple(condition.node for condition in conditions),
            )
        else:
            return conditions[0].node


def _get_node_duplicates_in_conditions(
    conditions: Iterable[Condition],
) -> Iterator[Node]:
    """Yield all nodes that will get duplicated when if-tests are created.

    For instance, if a conditioned block depends on `(cond1 and cond2) or not cond1`,
    then `cond1` is a duplicate, since it appears twice in that conditional.
    """
    # the next line groups conditions based on the node they depend on (`original_node`)
    # i.e., `node_usage_in_conditions` is a dictionary like:
    #
    # {
    #   node1: [condition1, condition2],
    #   node2: [condition2],
    #   node3: [condition1, condition3, condition4]
    # }
    #
    # in that situation, nodes `node1` and `node3` appear more than once in conditions.
    node_usage_in_conditions = groupby(
        conditions,
        key=lambda condition: condition.original_node,
    )
    return (
        node
        for node, conditions in node_usage_in_conditions.items()
        # only return nodes that appear in more than one condition
        if len(conditions) > 1
    )


def _get_conditions_in_test_for_conditioned_blocks(
    conditioned_blocks: List[ConditionedBlock],
) -> Iterator[Condition]:
    """Return all conditions that compose the test for `conditioned_blocks`."""
    return (
        condition
        for conditioned_block in conditioned_blocks
        if conditioned_block.block
        for condition in conditioned_block.conditions
    )
