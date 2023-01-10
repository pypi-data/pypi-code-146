"""Contains refactorings for if nodes."""
import typing
from typing import List, Tuple, Union

from sourcery.analysis.node_statements import NodeStatements
from sourcery.ast import (
    AST,
    Block,
    Compare,
    Continue,
    Elif,
    For,
    FunctionDef,
    If,
    Node,
    Raise,
    Return,
    While,
    is_pass_block,
)
from sourcery.ast.ast import invert_condition
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import GUARD_DESC, GUARD_ELIF


class GuardProposer(MultiProposer):
    """AST walker that proposed the various different guard clause refactorings."""

    node_statements: NodeStatements
    block_stack: List[List[Block]]

    LARGE_FUNCTION_SIZE = 10

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {LastIfGuardProposal, GuardProposal}

    def reset(self, ast: AST):
        super().reset(ast)
        self.block_stack = []

    def enter_if(self, node: If):
        self.block_stack.append([node.body])

    def enter_elif(self, node: Elif):
        self.block_stack[-1].append(node.body)

    def leave_if(self, node: If):
        current_blocks = self.block_stack.pop()

        if self.suitable_guard_extraction(node, current_blocks):
            for index, block in enumerate(current_blocks):
                if is_pass_block(block):
                    assert isinstance(block.parent, (If, Elif))
                    if self.conditions_disjoint(current_blocks[: index + 1]):
                        self.propose(GuardProposal(self.ast, block.parent, node))

    def suitable_guard_extraction(self, top_level_if: If, current_blocks: List[Block]):
        return (
            isinstance(top_level_if.parent.parent, (For, While, FunctionDef))
            and len(current_blocks) > 2
            and len(top_level_if.parent) == 1
        )

    def conditions_disjoint(self, blocks) -> bool:
        if len(blocks) == 1:
            return True

        conditions = [block.parent.test for block in blocks]
        return isinstance(conditions[0], Compare) and all(
            self.test_compares_value(condition, conditions[0].left) and condition
            for condition in conditions
        )

    def test_compares_value(self, node: Node, value: Node):
        return (
            isinstance(node, Compare)
            and len(node.comparators) == 1
            and node.ops[0] == Compare.EQ
            and hash(node.left) == hash(value)
        )

    def leave_functiondef(self, node: FunctionDef):
        if self.node_statements[node] <= self.LARGE_FUNCTION_SIZE:
            return

        if len(node.body) == 1 and isinstance(node.body[0], If):
            guard_if = node.body[0]
            if not guard_if.elifs:
                if not guard_if.orelse:
                    self.propose(LastIfGuardProposal(self.ast, guard_if, Return(None)))
                elif len(guard_if.orelse) == 1 and isinstance(
                    guard_if.orelse[0], (Raise, Return)
                ):
                    self.propose(
                        LastIfGuardProposal(self.ast, guard_if, guard_if.orelse[0])
                    )

        elif self.is_if_then_return(node.body):
            guard_if, guard_statement = node.body
            self.propose(LastIfGuardProposal(self.ast, guard_if, guard_statement))

    def is_if_then_return(self, block: Block):
        return (
            len(block) == 2
            and isinstance(block[0], If)
            and isinstance(block[1], Return)
            and not block[0].elifs
            and not block[0].orelse
            and isinstance(block[0].body[-1], Return)
        )


class LastIfGuardProposal(Proposal):
    """Proposal to create guard clause if function ends with an if."""

    def __init__(
        self, ast: AST, guard_if: If, guard_return: Union[Raise, Return]
    ) -> None:
        self.ast = ast
        self.guard_if = guard_if
        self.function_block = guard_if.parent
        self.guard_return = guard_return

    def description(self) -> str:
        return GUARD_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return (self.function_block,)

    def execute(self) -> None:
        if isinstance(self.function_block[-1], Return):
            self.function_block[-1:-1] = self.guard_if.body.statements
        else:
            self.function_block.extend(self.guard_if.body.statements)

        self.guard_if.test = invert_condition(self.guard_if.test)
        self.guard_if.body = Block((self.guard_return,))
        self.guard_if.orelse = Block(())

        if isinstance(self.function_block[-1], Return) and isinstance(
            self.function_block[-2], Return
        ):
            self.function_block.pop()


class GuardProposal(Proposal):
    """Proposal to create guard clause from a pass inside a big elif block."""

    def __init__(self, ast: AST, node: Union[If, Elif], top_level_if: If) -> None:
        self.ast = ast
        self.node = node
        self.top_level_if = top_level_if
        self.containing_parent = top_level_if.parent.parent
        self.index = self.top_level_if.parent.index(top_level_if)

    def description(self):
        return GUARD_ELIF

    def target_nodes(self) -> Tuple[Node, ...]:
        return self.top_level_if, self.node

    def execute(self) -> None:
        if isinstance(self.containing_parent, FunctionDef):
            guard_body = Block((Return(None),))
        else:
            guard_body = Block((Continue(),))

        if isinstance(self.node, If):
            first_elif, *rest = self.node.elifs

            guard = If(first_elif.test, first_elif.body, tuple(rest), self.node.orelse)
            self.top_level_if.parent.insert(self.index + 1, guard)

            self.node.body = guard_body
            self.node.elifs = ()
            self.node.orelse = Block(())
        else:
            assert isinstance(self.node, Elif)
            self.top_level_if.edit_tuple("elifs", lambda elifs: elifs.remove(self.node))
            guard = If(self.node.test, guard_body, (), Block(()))
            self.top_level_if.parent.insert(self.index, guard)
