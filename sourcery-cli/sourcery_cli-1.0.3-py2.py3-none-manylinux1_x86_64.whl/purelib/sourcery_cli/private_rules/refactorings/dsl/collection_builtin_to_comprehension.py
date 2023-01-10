from typing import List

from sourcery.ast import DictComp, GeneratorExp, ListComp, Node, SetComp, Tuple
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.rules.private.refactorings.descriptions import CALL_TO_COMP_DESC


class CollectionBuiltinToComprehensionProposer(DSLProposer):
    def create_code_changes(self) -> List[CodeChange]:
        # TODO These don't come out very intuitive
        return [
            CodeChange(
                pattern="list(${gen|isinstance(gen, GeneratorExp)})",
                replacement="${self.list_comprehension(gen)}",
            ),
            CodeChange(
                pattern="set(${gen|isinstance(gen, GeneratorExp)})",
                replacement="${self.set_comprehension(gen)}",
            ),
            CodeChange(
                pattern="dict(${gen|self.is_dict_generator(gen)})",
                replacement="${self.dict_comprehension(gen)}",
            ),
        ]

    def description(self) -> str:
        return CALL_TO_COMP_DESC

    def list_comprehension(self, node: Node) -> Node:
        assert isinstance(node, GeneratorExp)
        return ListComp(generators=node.generators, elt=node.elt)

    def set_comprehension(self, node: Node) -> Node:
        assert isinstance(node, GeneratorExp)
        return SetComp(generators=node.generators, elt=node.elt)

    def is_dict_generator(self, node: Node) -> bool:
        return (
            isinstance(node, GeneratorExp)
            and isinstance(node.elt, Tuple)
            and len(node.elt.elts) == 2
        )

    def dict_comprehension(self, node: Node) -> Node:
        assert isinstance(node, GeneratorExp)
        element = node.elt
        assert isinstance(element, Tuple)
        return DictComp(
            generators=node.generators,
            key=element.elts[0],
            value=element.elts[1],
        )
