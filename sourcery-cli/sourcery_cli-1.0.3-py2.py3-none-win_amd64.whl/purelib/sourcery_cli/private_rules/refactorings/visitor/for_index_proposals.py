import typing
from typing import Iterable, List, Set, Type

import inflect  # type: ignore

from sourcery.analysis.node_dependencies import Edge, NodeDependencies, VariableEdgeType
from sourcery.ast import (
    AST,
    Assign,
    Attribute,
    Call,
    Delete,
    Expression,
    For,
    Name,
    Node,
    Subscript,
    Tuple,
    get_nodes,
)
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.conditions.variable_usage_conditions import VariableUsageConditions
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    FOR_INDEX_DESC,
    USE_ITEMS_DESC,
)
from sourcery.semantic_equivalence.semantic_types import (
    LocalChangeOnException,
    LocalValueMissing,
    SemanticDifference,
)

BUILT_INS = list(__builtins__)


class ForIndexProposer(  # pylint: disable=too-many-ancestors
    MultiProposer, DependencyConditions, TypeConditions, VariableUsageConditions
):
    """AST walker that proposes refactorings of for loop indices.

    If they are for i in range(len(x)) and i is always used in x[i]
    then replace it. If the index isn't used use an underscore instead.
    """

    node_dependencies: NodeDependencies

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {ForIndexReplacementProposal, UseDictItemsProposal}

    def enter_for(self, node: For) -> None:
        outgoing = self.node_dependencies[node.target].outgoing.values()

        to_nodes = gather_to_nodes(outgoing)
        if self.indexed_for_loop(node):
            iterable = node.iter.args[0].args[0]  # type: ignore

            # Check that the iterable isn't written in the loop
            if iterable.unparse() in self.node_dependencies[node.body].all_writes():
                return

            if (
                all(
                    self.valid_index(to_node, node.target.unparse(), iterable)
                    for to_node in to_nodes
                )
                and self.has_list_type(iterable)
                and not self.is_accessed_later(node.target, node)
            ):
                self.propose(
                    ForIndexReplacementProposal(
                        self.ast, node, iterable, to_nodes, self.node_dependencies
                    )
                )

        elif self.has_dict_type(node.iter):
            for to_node in to_nodes:
                self.propose_dict_items(node, to_node)

    def propose_dict_items(self, node: For, to_node: Node) -> None:
        if self.is_value_reference(node, to_node):
            statement = to_node.statement()
            if not isinstance(statement, Delete):
                vars_in_scope = self.node_dependencies[
                    node.scope()
                ].all_reads_and_writes()

                if isinstance(statement, Assign):
                    if self.is_valid_assign(statement, to_node):
                        self.propose(
                            UseDictItemsProposal(
                                self.ast, node, statement, vars_in_scope
                            )
                        )
                else:
                    self.propose(
                        UseDictItemsProposal(self.ast, node, to_node, vars_in_scope)
                    )

    def is_value_reference(self, for_node: For, node: Node):
        return (
            isinstance(node, Name)
            and hash(node) == hash(for_node.target)
            and isinstance(node.parent, Subscript)
            and hash(node.parent.value) == hash(for_node.iter)
        )

    def is_valid_assign(self, statement: Assign, to_node: Node):
        target = get_single_assign_target(statement)
        return (
            target
            and isinstance(target, Name)
            and target.unparse() not in self.node_dependencies[statement].vars_in_scope
            and statement.value == to_node.parent
        )

    def indexed_for_loop(self, node: For):
        return (
            isinstance(node.iter, Call)
            and node.iter.func.unparse() == "range"
            and len(node.iter.args) == 1
            and isinstance(node.iter.args[0], Call)
            and node.iter.args[0].func.unparse() == "len"
        )

    def valid_index(self, index: Node, target: str, iterable: Node):
        if not self.index_of_list(index, target, iterable):
            return False

        statement = index.statement()
        # If we're assigning to the indexed iter it's a no-go
        if isinstance(statement, Assign):
            targets = get_nodes(statement.targets)
            parent_index_hash = hash(index.parent)
            return all(hash(target) != parent_index_hash for target in targets)
        # Can't replace an index reference if its a deletion
        elif isinstance(statement, Delete):
            return False
        else:
            return True

    def index_of_list(self, index: Node, target: str, iterable: Node):
        return (
            isinstance(index, Name)
            and index.unparse() == target
            and isinstance(index.parent, Subscript)
            and hash(index.parent.value) == hash(iterable)
        )


def gather_to_nodes(outgoing_edges: Iterable[Edge]) -> List[Node]:
    to_nodes: List[Node] = []
    for edge in outgoing_edges:
        for variable_edge_type in [
            edge_type
            for edge_type in edge.edge_types
            if isinstance(edge_type, VariableEdgeType)
        ]:
            to_nodes.extend([dep.node for dep in variable_edge_type.to_deps])
    return to_nodes


class ForIndexReplacementProposal(Proposal):
    """Proposal to replace index assignments in for loops with direct reference."""

    def __init__(
        self,
        ast: AST,
        for_node: For,
        iterable: Expression,
        to_nodes: List[Node],
        node_dependencies: NodeDependencies,
    ) -> None:
        self.ast = ast
        self.for_node = for_node
        self.to_nodes = to_nodes
        self.iterable = iterable
        self.node_dependencies = node_dependencies

    def description(self):
        return FOR_INDEX_DESC

    def target_nodes(self) -> typing.Tuple[Node, ...]:
        return (self.for_node,)

    def execute(self) -> None:
        vars_in_scope = self.node_dependencies[
            self.for_node.scope()
        ].all_reads_and_writes()

        self.for_node.iter = self.iterable

        iter_name = self.generate_name(vars_in_scope)
        replacement = Name(iter_name)

        for node in self.to_nodes:
            node.parent.replace(replacement)
        self.for_node.target = replacement

    def generate_name(self, vars_in_scope) -> str:
        if isinstance(self.for_node.iter, Attribute):
            iter_name = self.for_node.iter.attr.id
        else:
            iter_name = self.for_node.iter.unparse()

        sections = iter_name.split("_")
        if len(sections) > 1 and sections[-1] == "list":
            iter_name = "".join(sections[:-1])
        else:
            engine = inflect.engine()
            singular = engine.singular_noun(iter_name)
            iter_name = singular if singular and singular != iter_name else "item"
        return validated_name(iter_name, vars_in_scope)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {LocalValueMissing, LocalChangeOnException}


class UseDictItemsProposal(Proposal):
    """Proposal to use items() instead of direct assignment.

    for thing in things:
      detail = things[thing]
      ...
    ->
    for thing, detail in things.items():
      ...
    """

    def __init__(
        self, ast: AST, node: For, usage_node: Node, vars_in_scope: Set[str]
    ) -> None:
        self.ast = ast
        self.node = node
        self.usage_node = usage_node
        self.vars_in_scope = vars_in_scope

    def description(self):
        return USE_ITEMS_DESC

    def execute(self) -> None:
        if isinstance(self.usage_node, Assign):
            self.usage_node.parent.remove(self.usage_node)
            new_value = get_single_assign_target(self.usage_node)
        else:
            if self.node.target.unparse() == "k":
                value_name = validated_name("v", self.vars_in_scope)
            else:
                value_name = validated_name("value", self.vars_in_scope)
            new_value = Name(value_name)
            self.usage_node.parent.replace(Name(value_name))

        self.node.target = Tuple((self.node.target, new_value))

        new_iter = Call(Attribute(self.node.iter, Name("items")), ())
        self.node.iter = new_iter


def get_single_assign_target(assign: Assign):
    return assign.targets[0] if len(assign.targets) == 1 else None


def validated_name(name: str, vars_in_scope) -> str:
    while name in vars_in_scope or name in BUILT_INS:
        name += "_"
    return name
