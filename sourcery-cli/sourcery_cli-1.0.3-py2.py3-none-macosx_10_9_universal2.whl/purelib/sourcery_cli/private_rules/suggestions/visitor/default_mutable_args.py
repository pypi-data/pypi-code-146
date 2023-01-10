from typing import List

from sourcery.ast import AST, Assign, Block, Compare, Constant, Dict, FunctionDef, If
from sourcery.ast import List as Lst
from sourcery.ast import Param, Parameters, Set
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.engine.rule_type import RuleType


class DefaultMutableArgProposer(Proposer, DependencyConditions):
    def enter_parameters(self, node: Parameters):
        if mutable_args := [
            arg
            for arg in node.params
            if isinstance(arg.default, (Lst, Set, Dict))
            and not self.reads_any_variables(arg.default, arg.name)
        ]:
            self.propose(DefaultMutableArgProposal(self.ast, node, mutable_args))

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION


class DefaultMutableArgProposal(Proposal):
    def __init__(self, ast: AST, node: Parameters, mutable_args: List[Param]) -> None:
        self.ast = ast
        self.node = node
        self.mutable_args = mutable_args

    def description(self):
        return "Replace mutable default arguments with None"

    def execute(self) -> None:
        for arg in reversed(self.mutable_args):
            assert arg.default
            new_assign = Assign((arg.name,), arg.default)
            new_if = If(
                Compare(arg.name, (Compare.IS,), (Constant(None),)),
                Block((new_assign,)),
                (),
                Block(()),
            )
            arg.default = Constant(None)

            function_def = self.node.parent
            assert isinstance(function_def, FunctionDef)
            function_def.body.insert(0, new_if)

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION
