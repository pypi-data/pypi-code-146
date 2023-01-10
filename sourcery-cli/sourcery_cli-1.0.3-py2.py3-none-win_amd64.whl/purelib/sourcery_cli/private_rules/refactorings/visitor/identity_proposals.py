"""Contains refactorings for common code identities."""

import builtins
import typing
from typing import Dict, Optional, Set, Type, Union

from sourcery.ast import (
    AST,
    Assert,
    Assign,
    BinOp,
    Block,
    Call,
    Compare,
    Constant,
    Expression,
    If,
    IfExp,
    Name,
)
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    BIN_OP_DESC,
    FLIP_COMP_DESC,
    MINMAX_DESC,
    SIMPLIFY_COMP_DESC,
)
from sourcery.rules.private.refactorings.visitor.demorgan import INEQUALITY_OPS
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionRemoved,
    FunctionCallsOnException,
    SemanticDifference,
)

Identities = Dict[BinOp.Op, Optional[object]]


class IdentityProposer(MultiProposer, LiteralConditions, TypeConditions):
    """AST walker that proposed the various different identity refactorings."""

    none_compare_disabled: bool

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {
            BinOpIdentityProposal,
            FlipComparisonProposal,
            SimplifyNumericComparisonProposal,
            MinMaxIdentityProposal,
        }

    def reset(self, ast: AST):
        super().reset(ast)
        self.none_compare_disabled = False

    def enter_binop(self, node: BinOp):
        is_both_equal = node.left.unparse() == node.right.unparse()
        left_type = self.infer_type(node.left)

        if (
            is_both_equal
            and node.op in BinOpIdentityProposal.BASIC_IDENTITIES
            and left_type in BinOpIdentityProposal.BASIC_TYPES
        ):
            self.propose(BinOpIdentityProposal(self.ast, node, left_type))
        elif (
            is_both_equal
            and node.op in BinOpIdentityProposal.COMPLEX_IDENTITIES
            and left_type in BinOpIdentityProposal.COMPLEX_TYPES
        ):
            self.propose(BinOpIdentityProposal(self.ast, node, left_type))

    def enter_compare(self, node: Compare):
        if len(node.ops) == 1:
            if (
                self._is_flippable(node)
                # Asserts often have expected values on left
                and not isinstance(node.parent, Assert)
                and not isinstance(node.comparators[0], Constant)
            ):
                self.propose(FlipComparisonProposal(self.ast, node))
            elif self.can_simplify_compare(node):
                self.propose(SimplifyNumericComparisonProposal(self.ast, node))

    def _is_flippable(self, node: Compare):
        return (
            isinstance(node.left, Constant)
            and node.ops[0] in {Compare.EQ, Compare.NOT_EQ}
            or (self.is_numeric_literal(node.left) and node.ops[0] in INEQUALITY_OPS)
        )

    def can_simplify_compare(self, node: Compare):
        return (
            self.is_numeric_literal(node.comparators[0])
            and isinstance(node.left, BinOp)
            and node.left.op.invertible()
            and (
                (
                    node.left.op is not BinOp.DIV
                    and (
                        self.is_numeric_literal(node.left.left)
                        or self.is_numeric_literal(node.left.right)
                    )
                )
                or self.is_numeric_literal(node.left.right)
            )
        )

    def enter_if(self, node: If):
        if not node.orelse and self.can_propose_noelse_minmax(node):
            self.propose(MinMaxIdentityProposal(self.ast, node))

    def enter_ifexp(self, node: IfExp):
        if (
            isinstance(node.test, Compare)
            and self.is_valid_compare(node.test)
            and self.matching_vars(node.test, node.body, node.orelse)
        ):
            self.propose(MinMaxIdentityProposal(self.ast, node))

    def can_propose_noelse_minmax(self, node: If):
        return (
            isinstance(node.test, Compare)
            and self.is_valid_compare(node.test)
            and not node.elifs
            and not node.orelse
            and self.is_assign_block(node.body)
            and hash(node.test.left) == hash(node.body[0].targets[0])
            and hash(node.test.comparators[0]) == hash(node.body[0].value)
        )

    def is_valid_compare(self, test_node: Compare):
        return (
            len(test_node.ops) == 1
            and test_node.ops[0] in INEQUALITY_OPS
            and (
                self.has_simple_type(test_node.left)
                or self.has_simple_type(test_node.comparators[0])
            )
        )

    def is_assign_block(self, block: Block):
        return (
            len(block) == 1
            and isinstance(block[0], Assign)
            and len(block[0].targets) == 1
        )

    def matching_vars(
        self, test: Compare, body_expr: Expression, else_expr: Expression
    ):
        test_hashes = {hash(test.left), hash(test.comparators[0])}
        return {hash(body_expr), hash(else_expr)} == test_hashes


# TODO is operator overloading a problem here?
class BinOpIdentityProposal(Proposal):
    """Replaces binary ops between a value and itself with known identities.

    - `x | x` => x
    - `x & x` => x
    - `x ^ x` => 0
    - `x - x` => 0
    - `x / x` => 1
    - `x // x` => 1
    - `x % x` => 0
    """

    BASIC_TYPES = {"int", "float", "complex"}
    BASIC_IDENTITIES: Identities = {
        BinOp.SUB: 0,
        BinOp.DIV: 1,
        BinOp.FLOOR_DIV: 1,
        BinOp.MOD: 0,
    }

    COMPLEX_TYPES = {"int"}
    COMPLEX_IDENTITIES: Identities = {
        **BASIC_IDENTITIES,
        BinOp.BIT_OR: None,  # None means the operation is a noop: `x | x = x`
        BinOp.BIT_AND: None,
        BinOp.BIT_XOR: 0,
    }

    def __init__(self, ast: AST, node: BinOp, node_type: str) -> None:
        self.ast = ast
        self.node = node
        self.node_type = getattr(builtins, node_type)

    def description(self):
        return BIN_OP_DESC

    def execute(self) -> None:
        if self.node_type.__name__ in self.COMPLEX_TYPES:
            identity_set = self.COMPLEX_IDENTITIES
        else:
            identity_set = self.BASIC_IDENTITIES

        identity_value = identity_set[self.node.op]

        if identity_value is None:
            replacement = self.node.left
        else:
            replacement = Constant(value=self.node_type(identity_value))
            # for float 0, 0.0 and 1.0
            # for complex 0, 0j and 1+0j

        self.node.replace(replacement)


class FlipComparisonProposal(Proposal):
    """Flips a conditional to ensure the constant is on the right."""

    def __init__(self, ast: AST, node: Compare) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return FLIP_COMP_DESC

    def execute(self) -> None:
        self.node.left, self.node.comparators = (
            self.node.comparators[0],
            (self.node.left,),
        )
        self.node.ops = (self.node.ops[0].reverse(),)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged}


class SimplifyNumericComparisonProposal(Proposal, LiteralConditions):
    """Simplifies comparisons with consts on both sides.

    E.g if x + 1 == 2 -> if x == 1
    """

    # Removed BOOL_OP.And and BOOL_OP.Or due to short circuit eval
    COMMUTATIVE_NUMERIC_OPS = {
        BinOp.ADD,
        BinOp.MULT,
    }

    def __init__(self, ast: AST, node: Compare) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return SIMPLIFY_COMP_DESC

    def execute(self) -> None:
        # We know that the right of the compare is a number, and the left
        # is a binop where one of the values is a number.
        assert isinstance(self.node.left, BinOp)
        binop = self.node.left
        new_right_value = self.calculate_right_value(self.node)

        if self.is_numeric_literal(binop.right):
            self.alter_node(new_left=binop.left, new_right=new_right_value)
        elif self.node.left.op in self.COMMUTATIVE_NUMERIC_OPS:
            self.alter_node(new_left=binop.right, new_right=new_right_value)
        else:
            self.alter_node(new_left=new_right_value, new_right=binop.right)
            FlipComparisonProposal(self.ast, self.node).execute()

        if self.is_numeric_literal(binop.right) and binop.right.value < 0:
            self.node.ops = (self.node.ops[0].reverse(),)

    def alter_node(self, new_left: Expression, new_right: Expression):
        self.node.left = new_left
        self.node.ops = self.node.ops
        self.node.comparators = (new_right,)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ExceptionRemoved, FunctionCallsOnException, ExceptionArgsChanged}

    def calculate_right_value(self, node: Compare):
        binop = node.left
        assert isinstance(binop, BinOp)
        if self.is_numeric_literal(binop.right):
            return self._calculate_right_value(
                node.comparators[0], binop.right, binop.op.invert()
            )
        elif binop.op in self.COMMUTATIVE_NUMERIC_OPS and self.is_numeric_literal(
            binop.left
        ):
            return self._calculate_right_value(
                node.comparators[0], binop.left, binop.op.invert()
            )
        else:
            return self._calculate_right_value(
                binop.left, node.comparators[0], binop.op
            )

    def _calculate_right_value(
        self, left_side: Expression, right_side: Expression, operator: BinOp.Op
    ):
        # pylint: disable=unidiomatic-typecheck
        assert isinstance(left_side, Constant)
        assert isinstance(right_side, Constant)
        right_value = left_side.value
        binop_value = right_side.value
        new_right_value = operator(right_value, binop_value)

        # Convert to an int if unchanged
        if new_right_value == int(new_right_value):
            new_right_value = int(new_right_value)

        # Only do the substitution if the types are unchanged
        if type(new_right_value) == type(right_value):
            return Constant(new_right_value)
        else:
            return BinOp(left_side, operator, right_side)


class MinMaxIdentityProposal(Proposal):
    def __init__(self, ast: AST, node: Union[If, IfExp]) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return MINMAX_DESC

    def execute(self) -> None:
        compare_node = self.node.test
        assert isinstance(compare_node, Compare)

        value = (
            self.node.body if isinstance(self.node, IfExp) else self.node.body[0].value
        )
        flipped = hash(compare_node.left) != hash(value)

        if (compare_node.ops[0] in [Compare.LT, Compare.LTE]) != flipped:
            func = "min"
        else:
            func = "max"

        call = Call(
            func=Name(func),
            args=(compare_node.left, compare_node.comparators[0]),
        )

        if isinstance(self.node, IfExp):
            self.node.replace(call)
        else:
            self.node.replace(Assign(targets=self.node.body[0].targets, value=call))

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged}
