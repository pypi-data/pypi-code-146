"""Use f-string instead of string concatenation."""

from typing import List, Optional, Set, Type

from lib.version import PythonVersion
from sourcery.ast import (
    Attribute,
    BinOp,
    Call,
    Constant,
    Expression,
    FormattedValue,
    JoinedStr,
    Name,
    Node,
    Subscript,
    contains_node_meeting_condition,
)
from sourcery.code.source_unparser import MAX_LINE_LENGTH
from sourcery.conditions.f_string_conditions import FStringConditions
from sourcery.conditions.import_conditions import ImportConditions
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.semantic_equivalence.semantic_types import (
    ExceptionArgsChanged,
    ExceptionRemoved,
    LocalChangeOnException,
    ReturnValuesChangedOnException,
    SemanticDifference,
    StdOutChangedOnException,
)


class UseFstringForConcatenationProposer(  # pylint: disable=too-many-ancestors
    DSLProposer, FStringConditions, ImportConditions, LiteralConditions, TypeConditions
):
    ALLOWED_NODES = (Name, Attribute, Subscript, Call)

    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${a} + ${b}
                """,
                replacement="""
                    ${self._create_fstring(a, b)}
                """,
                top_level_condition=self._suitable_binop,
            ),
            CodeChange(
                pattern="""
                    ${a|isinstance(a, JoinedStr)} + ${b|self._is_allowed_single_node(b)}
                """,
                replacement="""
                    ${self._extend_fstring(a, b)}
                """,
                top_level_condition=self._binops_on_same_line,
            ),
            CodeChange(
                pattern="""
                    ${a|self._is_allowed_single_node(a)} + ${b|isinstance(b, JoinedStr)}
                """,
                replacement="""
                    ${self._extend_fstring(a, b)}
                """,
                top_level_condition=self._binops_on_same_line,
            ),
        ]

    def _suitable_binop(self, node: Optional[Node]) -> bool:
        # sourcery skip: assign-if-exp
        if not isinstance(node, BinOp):
            return False

        if not (
            self.is_valid_fstring_substring(node.left)
            or self.is_valid_fstring_substring(node.right)
        ):
            return False

        if not (self._allowed_node(node.left) or self._allowed_node(node.right)):
            return False

        return self._binops_on_same_line(node)

    def _binops_on_same_line(self, node: Optional[Node]) -> bool:
        if not isinstance(node, BinOp):
            return False

        if (
            node.left.lineno is not None
            and node.right.lineno is not None
            and node.left.lineno != node.right.lineno
        ):
            return False

        final_length = self._final_concatenated_fstring_length(node)

        return (
            # check if the final length does not exceed the maximum allowed line length
            # we obviously don't want to end up with overly long lines
            final_length < MAX_LINE_LENGTH - self._already_used_space_in_line(node.left)
            # also check if the final length is smaller than or as long as the original.
            # it is OK to exceed the maximum line length if we reduce (or at least keep
            # constant) the length of the already existing code
            # TODO: we need to replace `node.unparse()` with the original source code
            # for `node` because we may be losing whitespace information. For instance,
            # `"a+b"` will be parsed as an addition node, which is unparsed as
            # `"a + b"` (note the extra spaces)
            or final_length <= len(node.unparse())
        )

    def _final_concatenated_fstring_length(self, node: BinOp) -> int:
        extra_punctuation_length = (
            # if any of the operands is already an f-string, the only extra characters
            # that we are going to add are 2 brackets
            2  # 2 brackets
            if isinstance(node.left, JoinedStr) or isinstance(node.right, JoinedStr)
            # otherwise, we need to create a brand new f-string
            else 3  # "f"-prefix + 2 brackets
        )
        left_length = len(node.left.unparse())
        right_length = len(node.right.unparse())
        return left_length + right_length + extra_punctuation_length

    def _already_used_space_in_line(self, node: Node) -> int:
        return node.col_offset or 4  # default to assume 4 if we have no indent info

    def _is_allowed_single_node(self, node: Node) -> bool:
        return self.is_valid_fstring_substring(node) or self._allowed_node(node)

    # Disallow string constants so we aren't messing with mixing quote types
    # Also if we are using pandas ensure we have correctly inferred the types
    # are str.
    # TODO This isn't ideal - we should actually use type inference to check that this
    #      operation is OK.
    def _allowed_node(self, node: Node) -> bool:
        return (
            isinstance(node, self.ALLOWED_NODES)
            and not contains_node_meeting_condition(node, self.is_str_literal)
            and (self.has_str_type(node) or not self.has_module_name("pandas"))
        )

    def _create_fstring(self, left: Node, right: Node) -> JoinedStr:
        return JoinedStr(
            (self._wrap_node(left), self._wrap_node(right)),
            lineno=left.lineno,
            quote=getattr(left, "quote", getattr(right, "quote", None)),
        )

    def _extend_fstring(self, left: Node, right: Node) -> JoinedStr:
        if isinstance(left, JoinedStr):
            extended = left
            wrapped_node = self._wrap_node(right)
            extended.edit_tuple("values", lambda values: values.append(wrapped_node))
        else:
            assert isinstance(right, JoinedStr)
            extended = right
            wrapped_node = self._wrap_node(left)
            extended.edit_tuple("values", lambda values: values.insert(0, wrapped_node))
        return extended

    def _wrap_node(self, node: Node):
        assert isinstance(node, Expression)
        return node if isinstance(node, Constant) else FormattedValue(node, -1, None)

    def expected_semantic_differences(self) -> Set[Type[SemanticDifference]]:
        return {
            LocalChangeOnException,
            ExceptionRemoved,
            StdOutChangedOnException,
            ExceptionArgsChanged,
            ReturnValuesChangedOnException,
        }

    def description(self) -> str:
        return "Use f-string instead of string concatenation"

    def min_python_version(self) -> PythonVersion:
        return PythonVersion(major=3, minor=6)
