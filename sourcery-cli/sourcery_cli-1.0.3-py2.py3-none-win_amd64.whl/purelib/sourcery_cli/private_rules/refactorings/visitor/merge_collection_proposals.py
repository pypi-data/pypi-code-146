import typing
from typing import Optional, Set, Tuple, Type

from sourcery.analysis.node_dependencies import NodeDependencies
from sourcery.ast import AST, Assign, Attribute, Call
from sourcery.ast import Dict as Dct
from sourcery.ast import Expr
from sourcery.ast import List as Lst
from sourcery.ast import Name
from sourcery.ast import Set as St
from sourcery.ast import Slice, Starred, Statement, Subscript
from sourcery.ast import Tuple as Tpl
from sourcery.ast.ast import is_constant
from sourcery.ast.nodes import Expression, Node
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.engine.proposal import MultiProposer, Proposal
from sourcery.rules.private.refactorings.descriptions import (
    MERGE_APPEND_DESC,
    MERGE_DICT_DESC,
    MERGE_EXTEND_DESC,
    MERGE_SET_ADD_DESC,
)
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    LocalChangeOnException,
    SemanticDifference,
)


class MergeCollectionProposer(MultiProposer, TypeConditions):
    """Proposer that merges additions to collections with their declarations."""

    node_dependencies: NodeDependencies

    def possible_proposals(self) -> typing.Set[typing.Type[Proposal]]:
        return {
            MergeListAppendProposal,
            MergeListExtendProposal,
            MergeSetAddProposal,
            MergeDictAssignProposal,
        }

    def enter_expr(self, node: Expr):
        previous_assign = self.get_previous_assignment(node)
        if (
            previous_assign
            and isinstance(node.value, Call)
            and isinstance(node.value.func, Attribute)
            and self.is_matching_call(node.value, previous_assign)
            and not self.node_dependencies[previous_assign].writes_vars(
                self.node_dependencies[node.value.args[0]].all_reads_and_writes()
            )
        ):
            if node.value.func.attr.id == "add" and (
                previous_assign.value.unparse() == "set()"
                or isinstance(previous_assign.value, St)
            ):
                self.propose(MergeSetAddProposal(self.ast, previous_assign, node.value))
            elif isinstance(previous_assign.value, Lst):
                if node.value.func.attr.id == "append":
                    self.propose(
                        MergeListAppendProposal(self.ast, previous_assign, node.value)
                    )
                # Have to ensure what we're extending from is ordered
                elif node.value.func.attr.id == "extend" and self.has_type(
                    node.value.args[0], "dict", "list", "tuple"
                ):
                    self.propose(
                        MergeListExtendProposal(self.ast, previous_assign, node.value)
                    )

    def enter_assign(self, node: Assign):
        previous_assign = self.get_previous_assignment(node)
        if (
            previous_assign
            and is_matching_dict_assign(previous_assign, node)
            and not self.node_dependencies[previous_assign].writes_vars(
                self.node_dependencies[node.value].all_reads_and_writes()
            )
        ):
            self.propose(MergeDictAssignProposal(self.ast, previous_assign, node))

    def is_matching_call(self, node: Call, previous_assign: Assign) -> bool:
        return (
            isinstance(node.func, Attribute)
            and hash(node.func.value) == hash(previous_assign.targets[0])
            and len(node.args) == 1
        )

    def get_previous_assignment(self, node: Statement) -> Optional[Assign]:
        previous_sibling = node.previous_sibling()
        if (
            previous_sibling
            and isinstance(previous_sibling, Assign)
            and len(previous_sibling.targets) == 1
        ):
            return previous_sibling
        else:
            return None


def is_matching_dict_assign(prev_assign, current_statement) -> bool:
    return (
        isinstance(prev_assign.value, Dct)
        and isinstance(current_statement, Assign)
        and len(current_statement.targets) == 1
        and isinstance(current_statement.targets[0], Subscript)
        and not isinstance(current_statement.targets[0].slice, (Tpl, Slice))
        and hash(current_statement.targets[0].value) == hash(prev_assign.targets[0])
    )


class MergeListAppendProposal(Proposal):
    """Merge an append with a previous list assignment."""

    def __init__(self, ast: AST, node: Assign, append: Call) -> None:
        self.ast = ast
        self.node = node
        self.append = append

    def description(self):
        return MERGE_APPEND_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return self.node, self.append

    def execute(self) -> None:
        assert isinstance(self.append.parent, Statement)

        assert isinstance(self.node.value, Lst)
        self.node.value = Lst(self.node.value.elts + (self.append.args))  # type: ignore
        for elt in self.node.value.elts:
            elt.parent = self.node.value
        self.node.parent.remove(self.append.parent)
        self.node.value.clear_original_source(clear_children=True)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {LocalChangeOnException}


class MergeListExtendProposal(Proposal):
    """Merge an extend with a previous list assignment."""

    def __init__(self, ast: AST, node: Assign, extend: Call) -> None:
        self.ast = ast
        self.node = node
        self.extend = extend

    def description(self):
        return MERGE_EXTEND_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return self.node, self.extend

    def execute(self) -> None:
        assert isinstance(self.extend.parent, Statement)
        assert isinstance(self.node.value, Lst)

        if is_constant_sequence(self.extend.args[0]):
            assert isinstance(self.extend.args[0], (Lst, Tpl, St))
            self.node.value.edit_tuple(
                "elts",
                lambda elts: elts.extend(self.extend.args[0].elts),  # type: ignore
            )
            for elt in self.node.value.elts:
                elt.parent = self.node.value
        elif self.node.value.elts:
            assert isinstance(self.extend.args[0], Expression)
            starred = Starred(self.extend.args[0])
            starred.parent = self.node.value
            self.node.value.edit_tuple("elts", lambda elts: elts.append(starred))
        else:
            self.node.value.replace(Call(Name("list"), self.extend.args))

        self.node.parent.remove(self.extend.parent)
        self.node.value.clear_original_source(clear_children=True)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {LocalChangeOnException, ExceptionArgsChanged}


class MergeSetAddProposal(Proposal):
    """Merge an add with a previous set assignment."""

    def __init__(self, ast: AST, node: Assign, add: Call) -> None:
        self.ast = ast
        self.node = node
        self.add = add

    def description(self):
        return MERGE_SET_ADD_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return self.node, self.add

    def execute(self) -> None:
        assert isinstance(self.add.parent, Statement)

        if isinstance(self.node.value, St):
            new_element = self.add.args[0]
            if all(hash(new_element) != hash(elt) for elt in self.node.value.elts):
                self.node.value.edit_tuple(
                    "elts", lambda elts: elts.append(new_element)
                )
                new_element.parent = self.node.value
        else:
            self.node.value = St(self.add.args)  # type: ignore

        self.node.parent.remove(self.add.parent)
        self.node.value.clear_original_source(clear_children=True)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {LocalChangeOnException}


class MergeDictAssignProposal(Proposal):
    """Merge a dictionary assign with its previous declaration."""

    def __init__(self, ast: AST, node: Assign, add: Assign) -> None:
        self.ast = ast
        self.node = node
        self.add = add

    def description(self):
        return MERGE_DICT_DESC

    def target_nodes(self) -> Tuple[Node, ...]:
        return self.node, self.add

    def execute(self) -> None:
        # pylint: disable=cell-var-from-loop
        assert isinstance(self.add.targets[0], Subscript)

        assert isinstance(self.node.value, Dct)
        new_key = self.add.targets[0].slice
        new_value = self.add.value
        new_key.parent = self.node.value
        new_value.parent = self.node.value

        delete_indices = [
            i
            for i, key in enumerate(self.node.value.keys)
            if key and hash(key) == hash(new_key)
        ]
        for i in reversed(delete_indices):
            self.node.value.edit_tuple("keys", lambda keys: keys.pop(i))
            self.node.value.edit_tuple("values", lambda values: values.pop(i))

        self.node.value.edit_tuple("keys", lambda keys: keys.append(new_key))
        self.node.value.edit_tuple("values", lambda values: values.append(new_value))

        self.node.parent.remove(self.add)
        self.node.value.clear_original_source(clear_children=True)

    @classmethod
    def expected_semantic_differences(cls) -> Set[Type[SemanticDifference]]:
        return {LocalChangeOnException}


def is_constant_sequence(node: Node):
    """Check if given node is a built-in sequence type containing only constants."""
    return isinstance(node, (Lst, Tpl, St)) and all(map(is_constant, node.elts))
