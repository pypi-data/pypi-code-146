from typing import List

from sourcery.conditions import LiteralConditions
from sourcery.conditions.pandas_conditions import PandasConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType

# These functions are mentioned as "a common category" in the Pandas docs:
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sum.html
AGG_METHODS = {"sum", "min", "max", "idxmin", "idxmax"}


class ReplaceApplyWithMethodCallProposer(
    DSLProposer, PandasConditions, LiteralConditions
):  # pylint: disable=too-many-ancestors
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${df|self.is_dataframe_or_series(df)}.apply(${agg|self.is_str_literal(agg) and agg.value in AGG_METHODS})
                """,
                replacement="${df}.${agg}()",
                top_level_condition=lambda _: (self.has_pandas_import_name()),
            )
        ]

    def description(self) -> str:
        return "Replace `apply` with a `DataFrame` or `Series` method"

    def kind(self) -> RuleType:
        return RuleType.REFACTORING
