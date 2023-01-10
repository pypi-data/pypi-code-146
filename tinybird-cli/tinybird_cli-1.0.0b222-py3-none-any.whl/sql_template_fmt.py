import logging
from typing import List, Optional
from dataclasses import dataclass
from types import MethodType

from sqlfmt import api
from sqlfmt.mode import Mode
from sqlfmt.dialect import ClickHouse
from sqlfmt import actions
from sqlfmt.analyzer import Rule, group
from sqlfmt.line import Line
from sqlfmt.comment import Comment
from sqlfmt.node import Node
from sqlfmt.node_manager import NodeManager
from sqlfmt.token import Token, TokenType
from sqlfmt.jinjafmt import JinjaTag, JinjaFormatter


# This class extends and monkey patches https://github.com/tconbeer/sqlfm
INDENT = " " * 4


@dataclass
class TBLine(Line):
    @property
    def prefix(self) -> str:
        """
        Returns the whitespace to be printed at the start of this Line for
        proper indentation.

        Tinybird => This is overriden from the base Line because we want SQL inside a template to be indented
        https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/line.py#L92
        """
        prefix = INDENT * (self.depth[0] + self.depth[1])
        return prefix


def from_nodes(
    cls,
    previous_node: Optional[Node],
    nodes: List[Node],
    comments: List[Comment],
) -> "Line":
    """
    Creates and returns a new line from a list of Nodes. Useful for line
    splitting and merging.

    Tinybird => Monkey patched to use `TBLine` and our own indentation logic.
    """
    if nodes:
        line = TBLine(
            previous_node=previous_node,
            nodes=nodes,
            comments=comments,
            formatting_disabled=nodes[0].formatting_disabled or nodes[-1].formatting_disabled,
        )
    else:
        line = TBLine(
            previous_node=previous_node,
            nodes=nodes,
            comments=comments,
            formatting_disabled=previous_node.formatting_disabled if previous_node else False,
        )

    return line


def standardize_value(cls, token: Token) -> str:
    """
    Tinybird => Monkey patched to not lower keywords
    https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/node_manager.py#L215
    """
    if token.type in (
        TokenType.UNTERM_KEYWORD,
        TokenType.STATEMENT_START,
        TokenType.STATEMENT_END,
        TokenType.WORD_OPERATOR,
        TokenType.ON,
        TokenType.BOOLEAN_OPERATOR,
        TokenType.SET_OPERATOR,
    ):
        return " ".join(token.token.split())
    else:
        return token.token


def _format_jinja_node(self, node: Node, max_length: int) -> bool:
    """
    Format a single jinja tag. No-ops for nodes that
    are not jinja. Returns True if the node was blackened
    """
    if node.is_jinja:
        formatter = JinjaFormatter(TBMode())
        tag = JinjaTag.from_string(node.value, node.depth[0] + node.depth[1])

        if tag.code and formatter.use_black:
            tag.code, tag.is_blackened = formatter.code_formatter.format_string(
                tag.code,
                max_length=tag.max_code_length(max_length),
            )

            if '{%' in node.value:
                parts = tag.code.split('\n')
                prefix = INDENT * (node.depth[0] + node.depth[1])
                if len(parts) > 1:
                    tag.code = '\n'.join([f'{prefix if i != 0 else ""}{part}' for i, part in enumerate(parts)])

        node.value = str(tag)

        return tag.is_blackened

    else:
        return False


# Some monkey patching
Line.from_nodes = MethodType(from_nodes, Line)
NodeManager.standardize_value = MethodType(standardize_value, NodeManager)
JinjaFormatter._format_jinja_node = MethodType(_format_jinja_node, JinjaFormatter)


class TinybirdDialect(ClickHouse):
    """
    This is an extension of the base rules.

    We might need to override the base `word_operator` and `unterm_keyword` rules with some custom ClickHouse terms.

    For now we are just overriding the end blocks for `if` and `for` to work with Tornado templates.

    https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/dialect.py#L55
    """
    def __init__(self) -> None:
        super().__init__()

        override_rules = {
            'main': [],
            'jinja': [
                Rule(
                    name="jinja_if_block_end",
                    priority=203,
                    pattern=group(r"\{%-?\s*end\s*-?%\}"),
                    action=actions.raise_sqlfmt_bracket_error,
                ),
                Rule(
                    name="jinja_for_block_end",
                    priority=211,
                    pattern=group(r"\{%-?\s*end\s*-?%\}"),
                    action=actions.raise_sqlfmt_bracket_error,
                ),
            ]
        }

        for section in override_rules:
            for rule in override_rules[section]:
                for rr in self.RULES[section]:
                    if rr.name == rule.name:
                        self.RULES[section].remove(rr)
                        self.RULES[section].append(rule)
                        break


class TBMode(Mode):
    def __post_init__(self) -> None:
        """
        Tinybird => Overriden to use `TinybirdDialect`
        https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/mode.py#L31
        """
        self.dialect = TinybirdDialect()


def format_sql_template(sql, line_length=None):
    try:
        # https://github.com/tconbeer/sqlfmt/blob/c11775b92d8a45f0e91d871b81a88a894d620bec/src/sqlfmt/mode.py#L16-L29
        config = {'line_length': line_length or 80}

        mode = TBMode(**config)
        sql = sql.strip()
        return '%\n' + api.format_string(sql[1:], mode=mode).strip() if sql[0] == '%' else api.format_string(sql, mode=mode).strip()
    except Exception as e:
        logging.warning(f'sqlfmt error: {str(e)}')
        return sql
