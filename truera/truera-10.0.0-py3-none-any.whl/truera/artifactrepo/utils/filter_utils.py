import logging

from google.protobuf.struct_pb2 import \
    Value  # pylint: disable=no-name-in-module
import sqlparse
from sqlparse import tokens as T

from truera.protobuf.public.data import filter_pb2 as filter_pb
from truera.public.feature_influence_constants import SCORE_TYPE_TO_QOI
from truera.utils import filter_constants


class FilterExpressionParseError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


def parse_expression_to_filter_proto(filter: str, logger=None):
    logger = logger or logging.getLogger(__name__)
    logger.debug("-------------------")

    parsed_filter_statement = sqlparse.parse(filter)[0]
    tokens = parsed_filter_statement.tokens
    return visit(tokens, logger, dbg_indent="#", original_filter_string=filter)


# pylint: disable=no-member
def visit(token, logger, original_filter_string, dbg_indent=""):
    dbg_indent = dbg_indent + "  "
    if isinstance(token, sqlparse.sql.TokenList) or isinstance(token, list):
        if isinstance(token, sqlparse.sql.Comparison):
            # disregarding whitespace, the subexpr is shaped like:
            #    op
            #   /  \
            #  L    R
            # with the order in tokens being L, op, R
            non_whitespace_inner_expressions = non_whitespace_tokens(
                token.tokens
            )
            if len(non_whitespace_inner_expressions) != 3:
                raise FilterExpressionParseError(
                    f"Unexpected filter shape: Comparison should have a left side, right side, and operator token. Provided: {str(non_whitespace_inner_expressions)}"
                )
            inner_comparison = non_whitespace_inner_expressions[1]

            column_name = get_column_name_from(
                token.left,
                logger,
                original_filter_string,
                dbg_indent=dbg_indent
            )
            column_name, model_id = filter_constants.get_base_column_name_and_model_id_from_filter_column_name(
                column_name
            )
            comparison_type = map_str_to_filter_leaf_comparison_type(
                inner_comparison, logger, original_filter_string, dbg_indent
            )
            literal_value = get_literal_value(
                token.right,
                logger,
                original_filter_string,
                dbg_indent=dbg_indent
            )
            if column_name == filter_constants.FILTER_GROUND_TRUTH_NAME:
                filter_leaf = filter_pb.FilterLeaf(
                    value_type=filter_pb.FilterLeaf.FilterLeafValueType.
                    GROUND_TRUTH,
                    filter_type=comparison_type,
                    values=[literal_value]
                )
            elif column_name in filter_constants.FILTER_MODEL_OUTPUT_NAMES_TO_SCORE_TYPES:
                score_type = filter_constants.FILTER_MODEL_OUTPUT_NAMES_TO_SCORE_TYPES[
                    column_name]
                qoi = SCORE_TYPE_TO_QOI[score_type]
                filter_leaf = filter_pb.FilterLeaf(
                    value_type=filter_pb.FilterLeaf.FilterLeafValueType.OUTPUT,
                    filter_type=comparison_type,
                    values=[literal_value],
                    score_type=qoi,
                    model_id=model_id
                )
            else:
                filter_leaf = filter_pb.FilterLeaf(
                    value_type=filter_pb.FilterLeaf.FilterLeafValueType.
                    COLUMN_VALUE,
                    column_name=column_name,
                    filter_type=comparison_type,
                    values=[literal_value]
                )
            return filter_pb.FilterExpression(filter_leaf=filter_leaf)
        elif isinstance(token, sqlparse.sql.Parenthesis):
            logger.debug(dbg_indent + "Paren open.")

            non_whitespace_inner_expressions = non_whitespace_tokens(
                token.tokens
            )

            # Non whitespace is Punctuation '(', exprs..., Punctuation ')'
            if non_whitespace_inner_expressions[
                0].ttype != T.Punctuation and non_whitespace_inner_expressions[
                    0].value == "(":
                raise FilterExpressionParseError(
                    f"Unexpected filter shape: Paren expression should have first token be open paren. Provided: {str(non_whitespace_inner_expressions[0])}. Full provided filter expression: {original_filter_string}."
                )
            if non_whitespace_inner_expressions[
                -1].ttype != T.Punctuation and non_whitespace_inner_expressions[
                    -1].value == ")":
                raise FilterExpressionParseError(
                    f"Unexpected filter shape: Paren expression should have first token be open paren. Provided: {str(non_whitespace_inner_expressions[-1])}. Full provided filter expression: {original_filter_string}."
                )

            to_return = visit(
                non_whitespace_inner_expressions[1:-1],
                logger,
                original_filter_string,
                dbg_indent=dbg_indent
            )

            logger.debug(dbg_indent + "Paren close.")

            return to_return
        else:
            to_iterate = non_whitespace_tokens(
                token.tokens if isinstance(token, sqlparse.sql.
                                           TokenList) else token
            )

            if len(to_iterate) == 0:
                raise FilterExpressionParseError(
                    f"Unexpected filter shape: token list was empty. Did your filter contain a logical operator with an empty child? Full provided filter expression: {original_filter_string}."
                )

            if len(to_iterate) == 1:
                return visit(
                    to_iterate[0],
                    logger,
                    original_filter_string,
                    dbg_indent=dbg_indent[0:-2]
                )

            return visit_expression_list(
                to_iterate, logger, original_filter_string, dbg_indent
            )

    elif isinstance(token, sqlparse.sql.Token):
        # Devnote - this could be revisited depending on the solution to AB#2506 for how we deal
        # with bools. Bools are not in the sql standard but some implmentations support them.
        # For ones that don't, we allow expressions like "col1 != 1" and col1 would be a BIT or
        # TINYINT style type. Some implementations like snowflake allow filters like "WHERE a"
        # with this acting like a null test. We don't support this kind of filter at the moment.
        # Those kinds of expressions would end up here.
        raise FilterExpressionParseError(
            f"Unexpected token: Loose single tokens should not be reached. Token: {token.value}. Full provided filter expression: {original_filter_string}."
        )
    else:
        raise FilterExpressionParseError(
            f"Unexpected filter shape: tree contained type that was not list, TokenList, or Token. Type: {str(type(token))}. Full provided filter expression: {original_filter_string}."
        )


def non_whitespace_tokens(tokens):
    return [t for t in tokens if not t.is_whitespace]


# pylint: disable=no-member
def visit_expression_list(tokens, logger, original_filter_string, dbg_indent):
    # SQL operator precedence:
    #  level | Operators we have     |   Operators we don't have
    #    1   |                       |   ~
    #    2   |                       |   *, /, %
    #    3   |                       |   + (Positive), - (Negative), + (Addition), + (Concatenation),
    #        |                       |   - (Subtraction), & (Bitwise AND), ^ (Bitwise Exclusive OR),
    #        |                       |   | (Bitwise OR)
    #    4   | =, !=, <, <=, >, >=   |   <>, !>, !<
    #    5   |   NOT                 |
    #    6   |   AND                 |
    #    7   |   OR                  |   ALL, ANY, BETWEEN, IN, LIKE, SOME
    #    8   |                       |   = (assignment)
    if tokens[0].is_keyword and tokens[0].value.upper() == "NOT":
        logger.debug(dbg_indent + "Keyword: NOT")
        contents = visit(
            tokens[1:], logger, original_filter_string, dbg_indent=dbg_indent
        )

        to_return = filter_pb.FilterExpression(
            operator=filter_pb.FilterExpressionOperator.FEO_NOT
        )
        to_return.sub_expressions.append(contents)

        return to_return
    else:
        indexes_of_ands = [
            i for i in range(len(tokens))
            if isinstance(tokens[i], sqlparse.sql.Token) and
            tokens[i].is_keyword and tokens[i].value.upper() == "AND"
        ]

        if indexes_of_ands:
            left = tokens[:indexes_of_ands[0]]
            right = tokens[indexes_of_ands[0] + 1:]

            left_expr = visit(
                left, logger, original_filter_string, dbg_indent=dbg_indent
            )
            logger.debug(dbg_indent + "Keyword: AND")
            right_expr = visit(
                right, logger, original_filter_string, dbg_indent=dbg_indent
            )
            to_return = filter_pb.FilterExpression(
                operator=filter_pb.FilterExpressionOperator.FEO_AND
            )

            to_return.sub_expressions.append(left_expr)
            to_return.sub_expressions.append(right_expr)
            return to_return

        indexes_of_ors = [
            i for i in range(len(tokens))
            if isinstance(tokens[i], sqlparse.sql.Token) and
            tokens[i].is_keyword and tokens[i].value.upper() == "OR"
        ]

        if indexes_of_ors:
            left = tokens[:indexes_of_ors[0]]
            right = tokens[indexes_of_ors[0] + 1:]

            left_expr = visit(
                left, logger, original_filter_string, dbg_indent=dbg_indent
            )
            logger.debug(dbg_indent + "Keyword: OR")
            right_expr = visit(
                right, logger, original_filter_string, dbg_indent=dbg_indent
            )
            to_return = filter_pb.FilterExpression(
                operator=filter_pb.FilterExpressionOperator.FEO_OR
            )

            to_return.sub_expressions.append(left_expr)
            to_return.sub_expressions.append(right_expr)
            return to_return

        # sqlparse is a non-validating parser. This is good for us in some ways -- we can just feed in expressions
        # and mostly get good things out, but it also means that invalid expressions come out in ways that don't
        # make much sense.
        #
        # If we've gotten to this point, we're going to fail with an error. I've added special cases below to try to
        # make the errors better in common cases.

        # In the case where there is SELECT / WHERE clauses in the list, provide a better error.
        common_statement_tokens = [
            s for s in tokens
            if isinstance(s, sqlparse.sql.Token) and s.is_keyword and
            (s.value.upper() == "WHERE" or s.value.upper() == "SELECT")
        ]
        if len(common_statement_tokens) > 0:
            raise FilterExpressionParseError(
                f"Unexpected token: {common_statement_tokens[0].value}. The tokens SELECT / WHERE are not expected to occur since only filter expressions are allowed. Full provided filter expression: {original_filter_string}."
            )

        # We'll eventually supoort IN: AB#2504
        in_tokens = [
            s for s in tokens if isinstance(s, sqlparse.sql.Token) and
            s.is_keyword and s.value == "IN"
        ]
        if len(in_tokens) > 0:
            raise FilterExpressionParseError(
                f"Unexpected token: {in_tokens[0].value}. IN expressions are not supported. Full provided filter expression: {original_filter_string}."
            )

        # expressions starting with binary comparison operators - ie "< 5"
        if _is_binary_operator(tokens[0]):
            raise FilterExpressionParseError(
                f"Unexpected token: token list begins with binary operator {tokens[0].value}. Full provided filter expression: {original_filter_string}."
            )

        # expressions ending with binary comparison operators- ie "a >="
        if _is_binary_operator(tokens[-1]):
            raise FilterExpressionParseError(
                f"Unexpected token: token list ends with binary operator {tokens[-1].value}. Full provided filter expression: {original_filter_string}."
            )

        # Mismatched parens
        open_parens = [
            s for s in tokens if s.ttype == T.Punctuation and s.value == "("
        ]
        close_parens = [
            s for s in tokens if s.ttype == T.Punctuation and s.value == ")"
        ]

        if open_parens != close_parens:
            raise FilterExpressionParseError(
                f"Unexpected filter shape: mismatched number of left and right parens. There are {len(open_parens)} instances of '(' vs {len(close_parens)} instances of ')' in the offending subexpression. Full provided filter expression: {original_filter_string}."
            )

        # Finally - the default error.
        raise FilterExpressionParseError(
            f"Unexpected token: token list was not of known type, 'not', 'and', or 'or' expression. Type: {type(tokens)}. Full provided filter expression: {original_filter_string}."
        )


def _is_binary_operator(token):
    if isinstance(
        token, sqlparse.sql.Token
    ) and token.ttype == T.Operator.Comparison:
        return token.value in ["==", "!=", "<>", "<", "<=", ">", ">="]
    return False


def get_column_name_from(token, logger, original_filter_string, dbg_indent):
    dbg_indent = dbg_indent + "  "

    # expected: token is an Identifier with 1 element - the name
    if isinstance(token, sqlparse.sql.Identifier):
        logger.debug(dbg_indent + "Identifier: " + token.value)

        if len(token.tokens) != 1:
            raise FilterExpressionParseError(
                f"Unexpected filter shape: Identifier token list should have only one element. Provided: {str(token.tokens)}. Full provided filter expression: {original_filter_string}."
            )

        return dequotify_string(token.value)

    elif isinstance(
        token, sqlparse.sql.Token
    ):  # needs this so we can have feature name that only consists of numbers
        return dequotify_string(token.value)


# pylint: disable=no-member
def map_str_to_filter_leaf_comparison_type(
    token, logger, original_filter_string, dbg_indent
):
    logger.debug(dbg_indent + token.value)
    value = token.value
    if value in ["==", "="]:
        return filter_pb.FilterLeaf.FilterLeafComparisonType.EQUALS
    if value == "!=" or value == "<>":
        return filter_pb.FilterLeaf.FilterLeafComparisonType.NOT_EQUALS
    if value == "<":
        return filter_pb.FilterLeaf.FilterLeafComparisonType.LESS_THAN
    if value == "<=":
        return filter_pb.FilterLeaf.FilterLeafComparisonType.LESS_THAN_EQUAL_TO
    if value == ">":
        return filter_pb.FilterLeaf.FilterLeafComparisonType.GREATER_THAN
    if value == ">=":
        return filter_pb.FilterLeaf.FilterLeafComparisonType.GREATER_THAN_EQUAL_TO
    raise FilterExpressionParseError(
        f"Unexpected comparison type: {token.value}. Full provided filter expression: {original_filter_string}."
    )


def get_literal_value(token, logger, original_filter_string, dbg_indent):
    dbg_indent = dbg_indent + "  "
    if isinstance(token, sqlparse.sql.Token):
        if isinstance(
            token, sqlparse.sql.Token
        ) and token.ttype == T.Literal.String.Single:
            logger.debug(dbg_indent + "String Literal: " + token.value)
            return Value(string_value=dequotify_string_literal(token.value))
        if isinstance(
            token, sqlparse.sql.Token
        ) and token.ttype == T.Literal.Number.Integer:
            logger.debug(dbg_indent + "Int Literal: " + token.value)
            return Value(number_value=int(token.value))
        if isinstance(
            token, sqlparse.sql.Token
        ) and token.ttype == T.Literal.Number.Float:
            logger.debug(dbg_indent + "Float Literal: " + token.value)
            return Value(number_value=float(token.value))
        # sqlparse gives double quoted strings like "some_literal" as identifiers.
        if isinstance(token, sqlparse.sql.Identifier):
            logger.debug(dbg_indent + "String Identifier: " + token.value)
            if len(token.tokens) != 1:
                raise FilterExpressionParseError(
                    f"Unexpected filter shape: Identifier token list should have only one element. Provided: {str(token.tokens)}. Full provided filter expression: {original_filter_string}."
                )
            return Value(string_value=dequotify_string_literal(token.value))
        raise FilterExpressionParseError(
            f"Unexpected token: Token of type {token.ttype} or value {token.value} was not expected when getting literal value. Full provided filter expression: {original_filter_string}."
        )
    raise FilterExpressionParseError(
        f"Unexpected type: Expected type Token but was {type(token)}. Full provided filter expression: {original_filter_string}."
    )


def dequotify_string_literal(token_value: str) -> str:
    dequotified_token_value = dequotify_string(token_value)
    if dequotified_token_value == token_value:
        raise FilterExpressionParseError(
            f"Unexpected string literal! Expected literal to be encapsulated in single or double quotes but found: {token_value}"
        )
    return dequotified_token_value


def dequotify_string(token_value: str) -> str:
    if token_value.startswith('"') and token_value.endswith('"'):
        return token_value[1:-1]
    if token_value.startswith("'") and token_value.endswith("'"):
        return token_value[1:-1]
    return token_value
