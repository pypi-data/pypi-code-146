from typing import List, Union

from sourcery.ast.nodes import BinOp, Expression, Lambda, Name, Param
from sourcery.conditions.pandas_conditions import PandasConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class ReplaceApplyWithNumpyOperationProposer(
    DSLProposer, PandasConditions
):  # pylint: disable=too-many-ancestors
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${df|self.is_dataframe_or_series}.apply(${lambda_|is_vectorizable})
                """,
                replacement="""
                    ${self.simplified_binop(df, lambda_)}
                """,
                top_level_condition=lambda _: (self.has_pandas_import_name()),
            ),
        ]

    def is_vectorizable(self, lambda_: Union[Expression, str]) -> bool:
        """Determine whether the operation can be vectorized by using Numpy.

        Generally, the operation can be vectorized if the operands are numbers.

        Counterexamples, operations that can't be vectorized:
        * adding a Series to a DataFrame
        * string operations

        Out of scope for the current implementation:
        1) Calling user-defined functions in a lambda.
        Depending on the content of the function,
        these could be sometimes also vectorized.

        2) Providing a function name as apply's parameter.
        """
        if not isinstance(lambda_, Lambda) or len(lambda_.params.params) != 1:
            return False
        only_param = lambda_.params.params[0]
        binop_ = lambda_.body
        return (
            self._allowed_operand(binop_.left, only_param)
            and self._allowed_operand(binop_.right, only_param)
            if isinstance(binop_, BinOp)
            else False
        )

    def _allowed_operand(self, expr: Expression, param: Param) -> bool:
        if self._refers_to_param(expr, param) or self.has_numeric_type(expr):
            return True
        if isinstance(expr, BinOp):
            return self._allowed_operand(expr.left, param) and self._allowed_operand(
                expr.right, param
            )
        return False

    def simplified_binop(self, df: Name, lambda_: Lambda) -> BinOp:
        # We've checked these in the condition:
        assert isinstance(lambda_.body, BinOp)
        assert len(lambda_.params.params) == 1
        only_arg = lambda_.params.params[0]
        return self._convert_binop(lambda_.body, only_arg, df)

    def _convert_binop(self, binop_: BinOp, param: Param, replacement: Name) -> BinOp:
        if self._refers_to_param(binop_.left, param):
            binop_.left = replacement
        if self._refers_to_param(binop_.right, param):
            binop_.right = replacement
        if isinstance(binop_.left, BinOp):
            binop_.left = self._convert_binop(binop_.left, param, replacement)
        return binop_

    def _refers_to_param(self, expr: Expression, param: Param) -> bool:
        return isinstance(expr, Name) and expr.id == param.name.id

    def description(self) -> str:
        return "Replace apply with a NumPy operation"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
