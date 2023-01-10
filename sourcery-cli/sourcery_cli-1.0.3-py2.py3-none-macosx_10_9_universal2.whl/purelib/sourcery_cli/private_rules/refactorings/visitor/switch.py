"""Contains the switch refactoring."""
from collections import defaultdict
from typing import Dict, Hashable, List, Optional, Set, Tuple, Union

from sourcery.analysis.clone_detection import Hash, NodeClonesAnalyzer
from sourcery.analysis.node_dependencies import NodeDependencies
import sourcery.ast
from sourcery.ast import (
    AST,
    Attribute,
    Block,
    Break,
    Compare,
    Constant,
    Continue,
    Elif,
    ExceptHandler,
    Expression,
    For,
    FunctionDef,
    If,
    Name,
    Node,
    Pass,
    Raise,
    Return,
    Statement,
    UnaryOp,
)
from sourcery.ast.ast import body_breaks_flow
from sourcery.engine.proposal import Proposal, Proposer
from sourcery.rules.private.refactorings.descriptions import MERGE_SWITCH_DESC


class SwitchVariable:
    __slots__ = [
        "variable_name",
        "name_node",
        "outer_scopes",
        "is_valid",
        "switch_bodies",
        "else_body",
        "current_conditionals",
        "current_matching_bodies",
        "processed_nodes",
    ]
    ELSE_VALUE = hash(Node)

    def __init__(
        self,
        variable_name: str,
        outer_scope: If,
        name_node: Union[Attribute, Name],
    ) -> None:
        self.variable_name = variable_name
        self.name_node = name_node
        self.outer_scopes = [outer_scope]
        self.is_valid = True

        self.switch_bodies: Dict[SwitchableInfo, List[Statement]] = {}
        self.else_body: List[Statement] = []
        self.current_conditionals: List[SwitchableInfo] = []
        self.current_matching_bodies: List[List[Statement]] = []
        self.processed_nodes: Set[Node] = set()

    def mark_invalid(self) -> None:
        self.is_valid = False

    def add_switchable_condition(
        self, node: Union[If, Elif], info: "SwitchableInfo"
    ) -> None:
        if node.parent.parent not in self.processed_nodes:
            if info not in self.switch_bodies:
                self.switch_bodies[info] = list(self.else_body)
            self.current_conditionals.append(info)
            self.update_matching_values()

    def leave_switchable_condition(self, node: If) -> None:
        if node not in self.processed_nodes:
            self.current_conditionals.pop()
            self.update_matching_values()

    def invert_last_condition(self, node: If) -> None:
        if node not in self.processed_nodes:
            self.current_conditionals[-1] = self.current_conditionals[-1].invert()
            self.update_matching_values()

    def update_matching_values(self) -> None:
        def matches_current_conditions(value: Hash) -> bool:
            return all(cond.matches(value) for cond in self.current_conditionals)

        self.current_matching_bodies = [
            body
            for info, body in self.switch_bodies.items()
            if matches_current_conditions(info.value_hash)
        ]
        if matches_current_conditions(self.ELSE_VALUE):
            self.current_matching_bodies.append(self.else_body)

    def add_statement(self, statement: Statement) -> None:
        # Don't add if nodes for our variable as they are considered in
        # their own enter if method
        def can_add_node(node: Node) -> bool:
            if isinstance(node, (If, Elif)):
                info = SwitchableInfo.from_node(node.test)
                return not info or info.name != self.variable_name

            return not isinstance(node, Pass)

        # This statements has already been dealt with
        if statement.parent.parent in self.processed_nodes or (
            isinstance(statement.parent.parent, (Elif, ExceptHandler))
            and statement.parent.parent.parent in self.processed_nodes
        ):
            self.processed_nodes.add(statement)
        elif can_add_node(statement):
            self.processed_nodes.add(statement)
            for body in self.current_matching_bodies:
                body.append(statement)

    def conditional_bodies(
        self,
    ) -> List[Tuple[List[Expression], Block]]:
        switch_bodies: Dict[SwitchableInfo, Block] = {
            key: Block.create_virtual(value)
            for key, value in self.switch_bodies.items()
        }
        else_body = Block.create_virtual(self.else_body)

        node_clones = NodeClonesAnalyzer().node_clones(
            *switch_bodies.values(), else_body
        )

        block_values: Dict[Block, List[Expression]] = defaultdict(list)
        for info, body in switch_bodies.items():
            if clones := node_clones[body]:
                # Don't include branch if it is a duplicate of the else body
                if else_body not in clones:
                    # Use the first clone for all values
                    block_values[clones[0]].append(info.value)  # type: ignore
            else:
                block_values[body] = [info.value]

        return sorted(
            [(values, block) for block, values in block_values.items()],
            key=lambda x: self.get_string(x[0]),
        )

    def get_string(self, values: List[Expression]):
        return str([x.unparse() for x in values])


class SwitchProposer(Proposer):
    """Proposes switch refactoring.

    It has to build up a picture of which variables are in the if statement and
    where they are true before proposing a refactoring. It will also consider
    subsequent if statements.
    """

    node_dependencies: NodeDependencies
    variables: Dict[str, SwitchVariable] = {}

    def __init__(self, minimum_switch_statements=2) -> None:
        super().__init__()
        self.minimum_switch_statements = minimum_switch_statements

    def reset(self, ast: AST):
        super().reset(ast)
        self.variables = {}

    def enter_if(self, node: If):
        if not self.is_guard_clause(node):
            if info := SwitchableInfo.from_node(node.test):
                if info.name not in self.variables:
                    self.variables[info.name] = SwitchVariable(
                        info.name, node, info.name_node
                    )
                self.variables[info.name].add_switchable_condition(node, info)

        self.enter_statement(node)

    def enter_elif(self, node: Elif):
        # If we're adding this to the switch need to invert the
        # conditional before considering the eiif nodes
        info = SwitchableInfo.from_node(node.test)
        parent_info = SwitchableInfo.from_node(node.parent.test)

        if info and parent_info and info.name in self.variables:
            if (
                node.parent.parent.parent
                not in self.variables[info.name].processed_nodes
            ):
                self.variables[info.name].invert_last_condition(node.parent)
                self.variables[info.name].add_switchable_condition(node, info)
        elif parent_info:
            self.variables[parent_info.name].mark_invalid()

    def is_guard_clause(self, node: If):
        return (
            isinstance(node.body[0], (Break, Continue, Raise, Return))
            and isinstance(node.parent.parent, (FunctionDef, For))
            and not node.elifs
            and not node.orelse
        )

    def enter_statement(self, node: Statement):
        for variable in self.variables.values():
            variable.add_statement(node)

    def enter_block(self, node: Block):
        # If we're adding this to the switch need to invert the
        # conditional before considering the else nodes
        if isinstance(node.parent, If) and node.is_else_block():
            info = SwitchableInfo.from_node(node.parent.test)
            if info and info.name in self.variables:
                self.variables[info.name].invert_last_condition(node.parent)

    def leave_if(self, node: If):
        # Don't merge guard clauses
        if self.is_guard_clause(node):
            return

        # If we're adding this to the switch update the conditionals we're tracking
        info = SwitchableInfo.from_node(node.test)
        if info and info.name in self.variables:
            self.variables[info.name].leave_switchable_condition(node)

            for elif_ in node.elifs:
                elif_info = SwitchableInfo.from_node(elif_.test)
                if elif_info and elif_info.name == info.name:
                    self.variables[info.name].leave_switchable_condition(node)

        for var_name, variable in list(self.variables.items()):
            if variable.is_valid and node in variable.outer_scopes:
                next_sibling = node.next_sibling()
                if (
                    isinstance(next_sibling, If)
                    and self.check_dependency(node, variable.variable_name)
                    and self.next_sibling_switch_eligible(
                        next_sibling, variable.variable_name
                    )
                    and not body_breaks_flow(node)
                ):
                    variable.outer_scopes.append(next_sibling)
                else:
                    if len(
                        variable.switch_bodies
                    ) >= self.minimum_switch_statements and self.check_dependency(
                        node, variable.variable_name
                    ):
                        self.propose(SwitchProposal(self.ast, variable))
                    self.variables.pop(var_name)

    def next_sibling_switch_eligible(self, next_sibling: If, var_name: str):
        info = SwitchableInfo.from_node(next_sibling.test)
        return (
            info
            and info.name == var_name
            and self.check_dependency(next_sibling, var_name)
        )

    def check_dependency(self, node: If, var_name: str):
        deps = self.node_dependencies[node]
        return not deps.writes_vars({var_name})


class SwitchableInfo:
    ALLOWED_OPERATORS = {Compare.EQ, Compare.NOT_EQ}

    def __init__(
        self,
        name: str,
        op: Compare.Op,
        value: Expression,
        value_hash: Hash,
        name_node: Union[Attribute, Name],
    ) -> None:
        self.name = name
        self.op = op
        self.value = value
        self.value_hash = value_hash
        self.name_node = name_node

    def invert(self) -> "SwitchableInfo":
        return SwitchableInfo(
            self.name, self.op.invert(), self.value, self.value_hash, self.name_node
        )

    def matches(self, hash_value: Hash) -> bool:
        return self.op(hash_value, self.value_hash)

    def __eq__(self, other):
        # Ignore operator when comparing equality
        return self.name == other.name and self.value_hash == other.value_hash

    def __hash__(self):
        return hash(self.name) + self.value_hash

    def __str__(self):
        return f"{self.name} {self.op.value} {self.value.unparse()}"

    __repr__ = __str__

    @classmethod
    def from_node(cls, node: Node) -> Optional["SwitchableInfo"]:
        if isinstance(node, Compare):
            if isinstance(node.left, (Name, Attribute)):
                name = node.left.unparse()
                name_node = node.left
                op = node.ops[0]
                value = node.comparators[0]
                if op in cls.ALLOWED_OPERATORS and isinstance(value, Constant):
                    return SwitchableInfo(name, op, value, hash(value), name_node)
        elif isinstance(node, UnaryOp) and node.op == UnaryOp.NOT:
            if info := cls.from_node(node.operand):
                return info.invert()

        return None


class SwitchProposal(Proposal):
    """Merges a nested conditional into a switch-like statement."""

    def __init__(self, ast: AST, variable: SwitchVariable) -> None:
        self.ast = ast
        self.node = variable.outer_scopes[0]
        self.variable = variable
        self.replacement: Optional[If] = None

    def description(self):
        return MERGE_SWITCH_DESC

    def _hash_arguments(self) -> Hashable:
        return self.node, self.variable.variable_name

    def execute(self) -> None:
        if conditional_bodies := self.variable.conditional_bodies():
            self.replacement = self.node.replace(self.create_switch(conditional_bodies))
            if len(self.variable.outer_scopes) > 1:
                for node in self.variable.outer_scopes[1:]:
                    node.parent.remove(node)
        else:
            # In case where all values match the else remove the if
            # and replace it with the else statements.
            first_scope = self.variable.outer_scopes[0]
            first_scope_index = first_scope.parent.index(first_scope)

            for node in self.variable.outer_scopes:
                node.parent.remove(node)

            for node in reversed(self.variable.else_body):  # type: ignore
                replacement = node
                replacement.parent = self.node.parent
                self.node.parent.insert(first_scope_index, replacement)

    def create_switch(
        self, conditional_bodies: List[Tuple[List[Expression], Block]]
    ) -> If:
        (if_values, if_body), *elif_bodies = conditional_bodies

        return If(
            self.construct_test_node(if_values),
            body=if_body,
            elifs=tuple(
                Elif(self.construct_test_node(test), body or Block(()))
                for test, body in elif_bodies
            ),
            orelse=Block.create_virtual(self.variable.else_body),
        )

    def construct_test_node(self, values: List[Expression]) -> Compare:
        if len(values) == 1:
            return Compare(self.variable.name_node, (Compare.EQ,), (values[0],))

        value_list = sourcery.ast.List(tuple(values))
        return Compare(self.variable.name_node, (Compare.IN,), (value_list,))
