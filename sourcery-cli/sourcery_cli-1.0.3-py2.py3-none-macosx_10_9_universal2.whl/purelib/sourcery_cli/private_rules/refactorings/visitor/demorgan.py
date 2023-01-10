"""Contains refactorings for common logical identities."""
from typing import Dict, Set, Type

from sourcery.analysis.typing.statement_types import infer_type
from sourcery.ast import (
    AST,
    BoolOp,
    Call,
    Compare,
    FunctionDef,
    Name,
    UnaryOp,
    parent_coerces_to_bool,
)
from sourcery.ast.ast import invert_condition
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import DEMORGAN_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    SemanticDifference,
)

INEQUALITY_OPS = {Compare.LTE, Compare.LT, Compare.GT, Compare.GTE}


class DeMorganProposer(Proposer, TypeConditions):
    """AST walker that proposed refactorings based on logical identities."""

    demorgan_disabled: bool

    def reset(self, ast: AST):
        super().reset(ast)
        self.demorgan_disabled = False

    def enter_functiondef(self, node: FunctionDef):
        if node.name.id in ["__eq__", "__ne__"]:
            self.demorgan_disabled = True

    def leave_functiondef(self, node: FunctionDef):
        if node.name.id in ["__eq__", "__ne__"]:
            self.demorgan_disabled = False

    def enter_boolop(self, node: BoolOp):
        if (
            node.lineno == node.parent.lineno
            and isinstance(node.parent, UnaryOp)
            and node.parent.op == UnaryOp.NOT
        ):
            self.propose_demorgan(node.parent)

    def enter_compare(self, node: Compare):
        if (
            isinstance(node.parent, UnaryOp)
            and node.parent.op == UnaryOp.NOT
            and self._compare_can_be_inverted(node)
        ):
            self.propose_demorgan(node.parent)

    def _compare_can_be_inverted(self, node: Compare) -> bool:
        if len(node.ops) != 1:
            return False

        if node.ops[0] not in INEQUALITY_OPS:
            return True

        # If we can infer the type of one side is valid assume they both are
        return self.has_simple_type(node.left) or self.has_simple_type(
            node.comparators[0]
        )

    # Remove double negatives
    def enter_unaryop(self, node: UnaryOp):
        if (
            node.op == UnaryOp.NOT
            and isinstance(node.operand, UnaryOp)
            and node.operand.op == UnaryOp.NOT
        ):
            self.propose_demorgan(node)

    def propose_demorgan(self, node: UnaryOp):
        if not self.demorgan_disabled:
            self.propose(DeMorganProposal(self.ast, node, self.statement_types[node]))


class DeMorganProposal(Proposal):
    """Proposal to execute transformation according to De Morgan identities.

    - `not (p and q) == not p or not q`
    - `not (p or q) == not p and not q`
    """

    def __init__(self, ast: AST, node: UnaryOp, existing_types: Dict[str, str]) -> None:
        self.ast = ast
        self.node = node
        self.existing_types = existing_types

    def description(self):
        return DEMORGAN_DESC

    def execute(self) -> None:
        replacement = invert_condition(self.node.operand)
        if not (
            parent_coerces_to_bool(self.node)
            or infer_type(replacement, self.existing_types) == "bool"
        ):
            replacement = Call(Name("bool"), (replacement,))

        self.node.replace(replacement)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged}
