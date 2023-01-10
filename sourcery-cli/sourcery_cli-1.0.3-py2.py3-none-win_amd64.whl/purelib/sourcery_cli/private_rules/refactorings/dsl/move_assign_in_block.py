from typing import List, Set, Type, Union

from sourcery.ast import Attribute, Name, Node, Statement
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    SemanticDifference,
)


class MoveAssignInBlockProposer(DSLProposer, DependencyConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${target|isinstance(target, (Name, Attribute))} = ${
                        value|not self.writes_any_variables(value)
                    }
                    ${statements+}
                    ${destination|self.suitable_destination(destination, target)}
                """,
                replacement="""
                    ${statements}
                    ${target} = ${value}
                    ${destination}
                """,
            ),
        ]

    def suitable_destination(
        self, destination: Node, target: Union[Name, Attribute]
    ) -> bool:
        if not self.accesses_any_variables(destination, target):
            return False

        assert isinstance(destination, Statement), destination

        return self.can_be_moved_ahead_of(target.statement(), destination)

    def description(self) -> str:
        return "Move assignment closer to its usage within a block"

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {LocalChangeOnException}

    def transient(self, _node: Node) -> bool:
        return True
