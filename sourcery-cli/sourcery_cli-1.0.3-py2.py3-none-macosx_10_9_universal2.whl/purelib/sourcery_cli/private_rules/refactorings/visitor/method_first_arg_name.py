import abc
import typing

from typing_extensions import TypeGuard

from sourcery.analysis.node_scope import NodeScopes
from sourcery.ast import (
    AST,
    DictComp,
    FunctionDef,
    GeneratorExp,
    ListComp,
    Name,
    Node,
    Param,
    Parameters,
    SetComp,
)
from sourcery.code.code_location import ScopeType
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.engine.rule_type import RuleType


class MethodFirstArgNameProposer(MultiProposer, DependencyConditions):
    node_scopes: NodeScopes

    CLASS_METHODS = {
        "__new__",
        "__init_subclass__",
        "__class_getitem__",
    }

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {InstanceMethodFirstArgNameProposal, ClassMethodFirstArgNameProposal}

    def is_method_in_class(self, arguments_parent: Node) -> TypeGuard[FunctionDef]:
        grandparent_scope = self.node_scopes[arguments_parent].get(-1)
        return bool(
            grandparent_scope
            and grandparent_scope.type == ScopeType.CLASS
            and isinstance(arguments_parent, FunctionDef)
        )

    def has_any_decorator(self, function_def: FunctionDef, decorators: typing.Set[str]):
        function_decorators = {
            decorator.unparse().split("(")[0]
            for decorator in function_def.decorator_list
        }
        return bool(function_decorators & decorators)

    def can_rename_first_arg(
        self, function_def: FunctionDef, arg0_name: str, target_name: str
    ) -> bool:
        return arg0_name != target_name and not self.accesses_any_variables(
            function_def.body, Name(target_name)
        )


class InstanceMethodFirstArgNameProposer(MethodFirstArgNameProposer):
    def enter_parameters(self, params: Parameters):
        function_def = params.parent

        if not self.is_method_in_class(function_def):
            return

        if function_def.name.id in self.CLASS_METHODS:
            return

        # Decorators might mean this proposal is not valid (e.g. pydantic validators)
        if function_def.decorator_list:
            return

        if not params.params:
            return

        arg0_name = params.params[0].name.id
        if not self.can_rename_first_arg(function_def, arg0_name, "self"):
            return

        self.propose(
            InstanceMethodFirstArgNameProposal(self.ast, function_def, arg0_name)
        )


class ClassMethodFirstArgNameProposer(MethodFirstArgNameProposer):
    def enter_parameters(self, params: Parameters):
        function_def = params.parent

        if not self.is_method_in_class(function_def):
            return

        if not (
            self.has_any_decorator(function_def, {"@classmethod"})
            or function_def.name.id in self.CLASS_METHODS
        ):
            return

        if not params.params:
            return

        arg0_name = params.params[0].name.id
        if not self.can_rename_first_arg(function_def, arg0_name, "cls"):
            return

        self.propose(ClassMethodFirstArgNameProposal(self.ast, function_def, arg0_name))


class MethodFirstArgNameProposal(Proposal, abc.ABC):
    proper_name: typing.ClassVar[str]

    def __init__(self, ast: AST, function_def: FunctionDef, arg0_name: str):
        self.ast = ast
        self.node = function_def  # needed for default implementation of target
        self.function_def = function_def
        self.arg0_name = arg0_name

    def execute(self) -> None:
        _head, *tail = self.function_def.params.params or (None,)
        self.function_def.params.params = (
            Param(Name(self.proper_name), None, None),
            *tail,
        )
        rename_recursively(self.function_def.body, self.arg0_name, self.proper_name)

    def kind(self) -> RuleType:
        return RuleType.REFACTORING

    def is_semantic_improvement(self) -> bool:
        return True


class InstanceMethodFirstArgNameProposal(MethodFirstArgNameProposal):
    proper_name: typing.ClassVar[str] = "self"

    def description(self) -> str:
        return "The first argument to instance methods should be `self`"


class ClassMethodFirstArgNameProposal(MethodFirstArgNameProposal):
    proper_name: typing.ClassVar[str] = "cls"

    def description(self) -> str:
        return "The first argument to class methods should be `cls`"


def rename_recursively(node: Node, from_str: str, to_str: str) -> None:
    """Rename every ``Name`` matching ``from_str`` in ``Node`` as ``to_str``.

    If the function encounters a nested function definition, it will only recurse
    if ``from_str`` is not one of the arguments, as this would override the scope
    of the variable.
    """
    if is_variable(node) and node.id == from_str:
        node.id = to_str
    for child in node.get_children():
        if isinstance(child, FunctionDef):  # pragma: no cover
            # Check for ``from_str`` in the arguments. If present, skip recursion.
            arg_names: typing.Set[str] = {arg.name.id for arg in child.params.params}
            if from_str in arg_names:
                continue
        if isinstance(child, (ListComp, GeneratorExp, SetComp, DictComp)):
            target_names: typing.Set[str] = {
                name for comp in child.generators for name in get_names(comp)
            }
            if from_str in target_names:
                continue

        rename_recursively(child, from_str, to_str)


def get_names(node: Node):
    if isinstance(node, Name):
        yield node.id
    for child in node.get_children():
        yield from get_names(child)


def is_variable(node: Node) -> TypeGuard[Name]:
    return isinstance(node, Name) and not node.is_attr()
