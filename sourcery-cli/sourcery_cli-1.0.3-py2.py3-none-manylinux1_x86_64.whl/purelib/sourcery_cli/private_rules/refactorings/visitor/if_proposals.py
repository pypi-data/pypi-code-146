"""Contains refactorings for if nodes."""
import typing
from typing import Set, Tuple

from sourcery.analysis.clone_detection import NodeClones
from sourcery.analysis.node_dependencies import GLOBAL_STATE, NodeDependencies
from sourcery.analysis.node_paths import PathNodes
from sourcery.analysis.node_statements import NodeStatements
from sourcery.ast import (
    AST,
    Block,
    BoolOp,
    Compare,
    Elif,
    If,
    List,
    Node,
    UnaryOp,
    is_contained_in,
    is_pass_block,
)
from sourcery.ast.ast import breaks_flow, invert_condition
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    MERGE_INTO_ELIF_DESC,
    MERGE_REPEATED_IFS_DESC,
    REMOVE_PASS_ELIF_DESC,
    SPLIT_OR_IFS_DESC,
    SWAP_IFELSE_DESC,
    SWAP_NESTED_DESC,
)


class IfProposer(MultiProposer, DependencyConditions):
    """AST walker that proposed the various different if refactorings."""

    node_dependencies: NodeDependencies
    node_clones: NodeClones
    node_paths: PathNodes
    node_statements: NodeStatements

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {
            SwapIfElseBranchesProposal,
            SwapNestedIfsProposal,
            MergeRepeatedIfsProposal,
            RemovePassElifProposal,
            SplitOrIfsProposal,
            MergeElseIfIntoElifProposal,
        }

    def enter_if(self, node: If):
        if not node.elifs and node.orelse:
            if self.is_negative(node.test) or if_is_guard(
                node.orelse, node.body, self.node_statements
            ):
                self.propose(SwapIfElseBranchesProposal(self.ast, node))
        elif len(node.body) == 1 and not node.elifs:
            inner = node.body[0]
            if (
                isinstance(inner, If)
                and self.can_be_moved_past(inner, node)
                and not self.node_dependencies[node.test].reads_vars(
                    self.node_dependencies[inner.test].reads
                )
            ):
                self.propose(SwapNestedIfsProposal(self.ast, node))

        if self.can_split_if(node):
            self.propose(SplitOrIfsProposal(self.ast, node))

        if (
            node.parent.is_else_block()
            and len(node.parent) == 1
            and isinstance(node.parent.parent, If)
        ):
            # Don't merge if the parent if breaks flow
            parent_if = node.parent.parent
            if parent_if.elifs:
                previous_block = parent_if.elifs[-1].body
            else:
                previous_block = parent_if.body
            if not breaks_flow(previous_block.statements[-1]):
                self.propose(MergeElseIfIntoElifProposal(self.ast, node.parent.parent))

    def can_split_if(self, node: If):
        if (
            isinstance(node.test, BoolOp)
            and node.test.op == BoolOp.OR
            and len(node.test.values) == 2
        ):
            values = node.test.values
        elif (
            isinstance(node.test, Compare)
            and node.test.ops[0] == Compare.IN
            and isinstance(node.test.comparators[0], List)
            and len(node.test.comparators[0].elts) == 2
        ):
            values = node.test.comparators[0].elts
        else:
            values = ()

        for value in values:
            for clone_value in self.node_clones[value]:
                if is_contained_in(clone_value, node.body):
                    return True

        return False

    def is_negative(self, cond) -> bool:
        """Check if condition mostly contains negatives."""
        return (
            (isinstance(cond, UnaryOp) and cond.op == UnaryOp.NOT)
            or (
                isinstance(cond, Compare)
                and cond.ops[0] in [Compare.NOT_EQ, Compare.NOT_IN, Compare.IS_NOT]
            )
            or (
                isinstance(cond, BoolOp)
                and all(self.is_negative(value) for value in cond.values)
            )
        )

    def enter_block(self, block: Block):
        if block:
            for i, (child, next_child) in enumerate(zip(block, block[1:])):
                if (
                    isinstance(child, If)
                    and isinstance(next_child, If)
                    and self.can_merge_ifs(child, next_child)
                ):
                    self.propose(
                        MergeRepeatedIfsProposal(self.ast, child, next_child, i)
                    )

    def can_merge_ifs(self, if1: If, if2: If) -> bool:
        """Check that all if...elif conditions are identical in the 2 ifs.

        Also check that the first if doesn't write any variables read in the
        if conditions
        """
        if1_test_deps = self.node_dependencies[if1.test]
        if1_body_deps = self.node_dependencies[if1.body]
        if1_orelse_deps = self.node_dependencies[if1.orelse]

        if GLOBAL_STATE in if1_body_deps.all_writes():
            return False

        read_vars: Set[str] = set()

        if len(if1.elifs) != len(if2.elifs):
            return False

        # TODO Use more general method of checking tests are equivalent
        ifs = [(if1, if2)] + list(zip(if1.elifs, if2.elifs))  # type: ignore
        for if1_, if2_ in ifs:
            if if1_.test.unparse() != if2_.test.unparse():
                return False

            read_vars |= self.node_dependencies[if1_.test].reads.keys()

        return not (
            if1_test_deps.writes_vars(read_vars)
            or if1_body_deps.writes_vars(read_vars)
            or if1_orelse_deps.writes_vars(read_vars)
        )

    def enter_elif(self, node: Elif):
        if node == node.parent.elifs[-1] and is_pass_block(node.body):
            self.propose(RemovePassElifProposal(self.ast, node))


def if_is_guard(
    guard_body: Block, main_body: Block, node_statements: NodeStatements
) -> bool:
    return is_guard_body(guard_body) and node_statements[main_body] > 1


def is_guard_body(block: Block) -> bool:
    return len(block) == 1 and breaks_flow(block[0])


class SwapNestedIfsProposal(Proposal):
    """Swaps the conditions of nested if statements with no orelse blocks."""

    def __init__(self, ast: AST, node: If) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return SWAP_NESTED_DESC

    def execute(self) -> None:
        block = self.node.parent
        inner = self.node.body[0]

        # Bring inner to outside
        block[block.index(self.node)] = inner

        # Nest inner blocks in outer condition
        inner.body = self.nest_inner_block_in_if(inner.body)

        for elif_ in inner.elifs:
            elif_.body = self.nest_inner_block_in_if(elif_.body)

        if inner.orelse:
            inner.orelse = self.nest_inner_block_in_if(inner.orelse)

    def nest_inner_block_in_if(self, block: Block) -> Block:
        return Block((If(test=self.node.test, body=block, elifs=(), orelse=Block(())),))


class SwapIfElseBranchesProposal(Proposal):
    """Inverts the condition of an if node and swaps the body and orelse blocks."""

    def __init__(self, ast: AST, node: If) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return SWAP_IFELSE_DESC

    def transient(self) -> bool:
        return True

    def execute(self) -> None:
        self.node.test = invert_condition(self.node.test)

        # Swap if and else branches
        self.node.body, self.node.orelse = self.node.orelse, self.node.body


class RemovePassElifProposal(Proposal):
    """Removes elif if it's a pass and it's just before the else or there is no else."""

    def __init__(self, ast: AST, node: Elif) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return REMOVE_PASS_ELIF_DESC

    def execute(self) -> None:
        if self.node.parent.orelse:
            self.node.test = invert_condition(self.node.test)
            self.node.body = self.node.parent.orelse
            self.node.parent.orelse = Block(())
        else:
            self.node.parent.edit_tuple("elifs", lambda elifs: elifs.pop())


class MergeRepeatedIfsProposal(Proposal):
    """Merges 2 consecutive if statements with the same condition into a single if."""

    def __init__(self, ast: AST, if1: If, if2: If, if_index: int) -> None:
        self.ast = ast
        self.if1 = if1
        self.if2 = if2
        self.if_index = if_index

    def description(self):
        return MERGE_REPEATED_IFS_DESC

    def execute(self) -> None:
        # Remove first if statement from block and replace second if statement
        self.if1.parent.pop(self.if_index)
        self.if1.parent[self.if_index] = self.merged_if(self.if1, self.if2)

    def target_nodes(self) -> Tuple[Node, ...]:
        return (self.if1, self.if2)

    def merged_if(self, if1: If, if2: If) -> If:
        elifs = tuple(
            Elif(elif1.test, body=elif1.body + elif2.body)
            for elif1, elif2 in zip(if1.elifs, if2.elifs)
        )
        return If(
            test=if1.test,
            body=if1.body + if2.body,
            elifs=elifs,
            orelse=if1.orelse + if2.orelse,
        )


class SplitOrIfsProposal(Proposal):
    """Splits an `or` conditional in an `if` out into separate if..elif branches."""

    def __init__(self, ast: AST, node: If) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return SPLIT_OR_IFS_DESC

    def execute(self) -> None:
        if isinstance(self.node.test, Compare):
            first_comp, second_comp = self.node.test.comparators[0].elts  # type: ignore
            first_test = self.node.test
            first_test.ops = (Compare.EQ,)
            first_test.comparators = (first_comp,)
            second_test = first_test.copy_as_root()
            second_test.ops = (Compare.EQ,)
            second_test.comparators = (second_comp,)
        else:
            first_test, second_test = self.node.test.values  # type: ignore
            # splitting out bracketed multiline tests causes issues
            if (
                self.node.test.lineno
                and self.node.lineno
                and self.node.test.lineno > self.node.lineno
            ):
                first_test.clear_original_source()
                second_test.clear_original_source()

        self.node.test = first_test

        new_elif = Elif(test=second_test, body=self.node.body)
        self.node.edit_tuple("elifs", lambda elifs: elifs.insert(0, new_elif))


class MergeElseIfIntoElifProposal(Proposal):
    """Merge else: if: into elif statement."""

    def __init__(self, ast: AST, node: If) -> None:
        self.ast = ast
        self.node = node

    def description(self) -> str:
        return MERGE_INTO_ELIF_DESC

    def execute(self) -> None:
        inner_if: If = self.node.orelse.statements[0]  # type: ignore
        extra_elifs = (Elif(inner_if.test, inner_if.body), *inner_if.elifs)
        self.node.edit_tuple("elifs", lambda elifs: elifs.extend(extra_elifs))
        for elif_ in self.node.elifs:
            elif_.parent = self.node
        self.node.orelse.replace(inner_if.orelse)
