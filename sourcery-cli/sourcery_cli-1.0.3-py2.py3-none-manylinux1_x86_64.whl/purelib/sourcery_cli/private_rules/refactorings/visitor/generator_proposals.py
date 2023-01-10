import typing
from typing import Set, Type

from sourcery.ast import (
    AST,
    Attribute,
    Call,
    Compare,
    Constant,
    Expression,
    GeneratorExp,
    ListComp,
    Name,
    Node,
    UnaryOp,
)
from sourcery.ast.ast import invert_condition
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    COMP_TO_GEN_DESC,
    INVERT_ANYALL_BODY_DESC,
    INVERT_ANYALL_DESC,
    SIMPLIFY_GEN_DESC,
)
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    FunctionCallsChanged,
    SemanticDifference,
)

GENERATOR_FUNCS = [
    "all",
    "any",
    "bytes",
    "enumerate",
    "frozenset",
    "list",
    "max",
    "min",
    "set",
    "sum",
    "tuple",
]


class GeneratorProposer(MultiProposer):
    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {
            ComprehensionToGeneratorProposal,
            SimplifyGeneratorProposal,
            InvertAnyAllBodyProposal,
            InvertAnyAllProposal,
        }

    def enter_listcomp(self, node: ListComp):
        if self._in_generator_call(node) and not any(
            gen.is_async for gen in node.generators
        ):
            self.propose(ComprehensionToGeneratorProposal(self.ast, node))

    def enter_generatorexp(self, node: GeneratorExp):
        if self._is_identity_generator(node, node.elt):
            wrap_in_iter = not (
                self._in_generator_call(node) or self._is_join(node.parent)
            )
            self.propose(
                SimplifyGeneratorProposal(
                    self.ast, node, node.generators[0].iter, wrap_in_iter
                )
            )

    def _in_generator_call(self, node: Node):
        return (
            isinstance(node.parent, Call)
            and node.parent.func.unparse() in GENERATOR_FUNCS
        )

    def _is_join(self, node: Node):
        return (
            isinstance(node, Call)
            and isinstance(node.func, Attribute)
            and node.func.attr.id == "join"
            and isinstance(node.func.value, Constant)
            and node.func.value.type == str
        )

    def enter_call(self, node: Call):
        if len(node.args) != 1:
            return

        arg = node.args[0]

        if node.func.unparse() in {"any", "all"} and isinstance(arg, GeneratorExp):
            if isinstance(node.parent, UnaryOp) and (
                isinstance(arg.elt, UnaryOp)
                or isinstance(arg.elt, Compare)
                and len(arg.elt.comparators) == 1
            ):
                self.propose(InvertAnyAllProposal(self.ast, node, arg.elt))
            elif self._is_inverse_generator(arg):
                self.propose(
                    InvertAnyAllBodyProposal(self.ast, node, arg.generators[0].iter)
                )

    def _is_inverse_generator(self, generator: GeneratorExp):
        return (
            isinstance(generator.elt, UnaryOp)
            and generator.elt.op is UnaryOp.NOT
            and self._is_identity_generator(generator, generator.elt.operand)
        )

    def _is_identity_generator(self, node: GeneratorExp, elt: Expression):
        if isinstance(elt, Name) and len(node.generators) == 1:
            generator = node.generators[0]
            return not generator.ifs and hash(generator.target) == hash(elt)
        return False


class ComprehensionToGeneratorProposal(Proposal):
    """Converts a comprehension to a generator where it wasn't needed."""

    def __init__(self, ast: AST, node: ListComp) -> None:
        self.ast = ast
        self.node = node

    def description(self):
        return COMP_TO_GEN_DESC

    def execute(self) -> None:
        replacement = GeneratorExp(self.node.generators, self.node.elt)
        self.node.replace(replacement)


class SimplifyGeneratorProposal(Proposal):
    """Proposal to execute transformation according to following identities.

    - `(a for a in things) -> (things)`
    """

    def __init__(
        self, ast: AST, node: GeneratorExp, iterator: Expression, wrap_in_iter: bool
    ) -> None:
        self.ast = ast
        self.node = node
        self.iterator = iterator
        self.wrap_in_iter = wrap_in_iter

    def description(self):
        return SIMPLIFY_GEN_DESC

    def execute(self) -> None:
        new_iterator = self.iterator
        if self.wrap_in_iter:
            new_iterator = Call(Name("iter"), (new_iterator,))
        self.node.replace(new_iterator)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        # TODO Should this FunctionCallsChanged be allowed?
        return {FunctionCallsChanged, ExceptionArgsChanged}


class InvertAnyAllBodyProposal(Proposal):
    """Proposal to execute transformation according to following identities.

    - `any(not a for a in things) == not all(things)`
    - `all(not a for a in things) == not any(thing)`
    """

    saved_call: Call
    replacement: UnaryOp

    def __init__(self, ast: AST, node: Call, iterable: Expression) -> None:
        self.ast = ast
        self.node = node
        self.iterable = iterable

    def description(self):
        return INVERT_ANYALL_BODY_DESC

    def execute(self) -> None:
        name = "all" if self.node.func.unparse() == "any" else "any"
        node = self.node.copy_as_root()
        node.func = Name(name)
        node.args = (self.iterable,)
        self.node.replace(UnaryOp(UnaryOp.NOT, node))


class InvertAnyAllProposal(Proposal):
    """Proposal to execute transformation according to following identities.

    - `not any(a == b for a in x) == all(a != b for a in x)`
    - 'not all(a == b for a in x) == any(a != b for a in x)
    """

    def __init__(self, ast: AST, node: Call, condition: Expression) -> None:
        self.ast = ast
        self.node = node
        self.condition = condition

    def description(self):
        return INVERT_ANYALL_DESC

    def execute(self) -> None:
        name = "all" if self.node.func.unparse() == "any" else "any"
        self.node.func = Name(name)
        self.condition.replace(invert_condition(self.condition.copy_as_root()))
        self.node.parent.replace(self.node)
