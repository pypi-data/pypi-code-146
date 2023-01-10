from typing import Any, Optional, Set, Type, Union

from sourcery.analysis.typing.statement_types import StatementTypes
from sourcery.ast import (
    AST,
    Assign,
    Attribute,
    AugAssign,
    BinOp,
    Expression,
    Name,
    Subscript,
    is_single_target_assign,
)
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import AUG_ASSIGN_DESC
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    SemanticDifference,
)

AUGASSIGN_TYPES = ["str", "int", "float", "bytes", "list"]


class AugAssignProposer(Proposer):
    # 'abc' + 'def' is not commutative
    COMMUTATIVE_OPS = [BinOp.MULT, BinOp.BIT_AND, BinOp.BIT_OR, BinOp.BIT_XOR]
    statement_types: StatementTypes

    def enter_assign(self, node: Assign) -> None:
        if (
            is_single_target_assign(node)
            and isinstance(node.targets[0], (Attribute, Name, Subscript))
            and isinstance(node.value, BinOp)
            and self.is_valid_augassign_target(node)
        ):
            if aug_assign_value := self.valid_augassign_value(
                node.targets[0], node.value
            ):
                self.propose(AugAssignProposal(self.ast, node, aug_assign_value))

    def is_valid_augassign_target(self, node: Assign) -> bool:
        variable = node.targets[0].unparse()

        # TODO: how can this be moved to `TypeConditions`?
        # Replacing this with `self.infer_type(node) in AUGASSIGN_TYPES` fails the
        # tests `test_complex_aug_assign` and `test_neg_aug_assign` because the typing
        # for and indexed item (`self.places[self.current_player]`) is not correctly
        # handled
        return (
            variable in self.statement_types[node]
            and self.statement_types[node][variable] in AUGASSIGN_TYPES
        )

    def valid_augassign_value(
        self, target: Union[Attribute, Name, Subscript], value: BinOp
    ) -> Optional[Expression]:
        target_str = target.unparse()
        if target_str == value.left.unparse():
            return value.right
        elif value.op in self.COMMUTATIVE_OPS and target_str == value.right.unparse():
            return value.left
        else:
            return None


class AugAssignProposal(Proposal):
    """Converts self assignments with binops to aug assignments.

    e.g x = x + 1 to x += 1
    """

    def __init__(self, ast: AST, node: Assign, aug_assign_value: Any) -> None:
        self.ast = ast
        self.node = node
        self.aug_assign_value = aug_assign_value

    def description(self):
        return AUG_ASSIGN_DESC

    def execute(self) -> None:
        assert isinstance(self.node.value, BinOp)

        self.node.replace(
            AugAssign(
                target=self.node.targets[0],
                op=self.node.value.op,
                value=self.aug_assign_value,
            )
        )

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {ExceptionArgsChanged}
