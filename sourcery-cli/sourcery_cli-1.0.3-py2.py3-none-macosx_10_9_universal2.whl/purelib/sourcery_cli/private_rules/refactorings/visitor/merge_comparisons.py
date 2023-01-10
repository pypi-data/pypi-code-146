from typing import Any, List

from sourcery.ast import AST, BoolOp, Compare, Constant, Expression
from sourcery.ast import List as Lst
from sourcery.ast import Node
from sourcery.ast import Set as St
from sourcery.ast import Tuple as Tpl
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import MERGE_COMPARISON_DESC

COLLECTION_TYPES = (Lst, St, Tpl)


class MergeComparisonsProposer(Proposer):
    """Merges and simplifies boolean comparisons."""

    def enter_boolop(self, node: BoolOp):
        if (
            self.valid_boolop(node)
            and self.all_compare_same_value(node)
            and not self.forbidden_combination(node)
        ):
            self.propose(MergeComparisonsProposal(self.ast, node))

    def valid_boolop(self, node: BoolOp):
        return (
            (
                node.op == BoolOp.OR
                and all(self.valid_eq_node(value) for value in node.values)
            )
            or node.op == BoolOp.AND
            and all(self.valid_ne_node(value) for value in node.values)
        )

    def valid_eq_node(self, node: Node):
        return (
            isinstance(node, Compare)
            and len(node.ops) == 1
            and (
                node.ops[0] == Compare.EQ
                or (
                    node.ops[0] == Compare.IN
                    and isinstance(node.comparators[0], COLLECTION_TYPES)
                )
            )
        )

    def valid_ne_node(self, node: Node):
        return (
            isinstance(node, Compare)
            and len(node.ops) == 1
            and (
                node.ops[0] == Compare.NOT_EQ
                or (
                    node.ops[0] == Compare.NOT_IN
                    and isinstance(node.comparators[0], COLLECTION_TYPES)
                )
            )
        )

    def all_compare_same_value(self, node: BoolOp):
        return all(
            hash(value.left) == hash(node.values[0].left)  # type: ignore
            for value in node.values
        )

    def forbidden_combination(self, node: BoolOp):
        # pylint: disable=unidiomatic-typecheck
        collections: List[Expression] = []
        others: List[Expression] = []
        for value_node in node.values:
            assert isinstance(value_node, Compare)
            if value_node.ops[0] in {Compare.EQ, Compare.NOT_EQ}:
                others.append(value_node.comparators[0])
            else:
                collections.append(value_node.comparators[0])
        # Cannot merge dissimilar collection types
        if any(type(collection) != type(collections[0]) for collection in collections):
            return True

        # Cannot merge non-contants into sets

        return any(
            isinstance(collection, St) for collection in collections
        ) and not all(isinstance(other, Constant) for other in others)


class MergeComparisonsProposal(Proposal):
    """Merge comparisons of the same variable into checking whether it is in a list."""

    def __init__(self, ast: AST, node: BoolOp) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return MERGE_COMPARISON_DESC

    def execute(self) -> None:
        left = self.node.values[0].left  # type: ignore
        comparators: List[Expression] = []
        collection_type: Any = Lst
        for node in self.node.values:
            assert isinstance(node, Compare)
            if node.ops[0] in {Compare.IN, Compare.NOT_IN}:
                collection_type = type(node.comparators[0])
            comparators.extend(self.get_comparators(node))

        op = Compare.IN if self.node.op == BoolOp.OR else Compare.NOT_IN
        compare = Compare(left, (op,), (collection_type(tuple(comparators)),))

        self.node.replace(compare)

    def get_comparators(self, node: Compare):
        if node.ops[0] in [Compare.EQ, Compare.NOT_EQ]:
            return [node.comparators[0]]

        assert node.ops[0] in [Compare.IN, Compare.NOT_IN]
        return node.comparators[0].elts  # type: ignore
