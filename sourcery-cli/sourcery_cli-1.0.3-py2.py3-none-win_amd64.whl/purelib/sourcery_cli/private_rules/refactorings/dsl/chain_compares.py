import typing
from typing import List

from sourcery.ast import Compare
from sourcery.conditions.dependency_conditions import DependencyConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class ChainComparesProposer(DSLProposer, DependencyConditions):
    def create_code_changes(self) -> List[CodeChange]:
        # TODO When $compare{...} syntax is available rework this so there's
        # only a single CodeChange instead of lots

        # These must be a chain of the same operator
        # e.g. a == b == c but not a == b != c
        same_op_changes = [
            self._code_change_for_comp_pair(comp.value, comp.value)
            for comp in (
                Compare.EQ,
                Compare.NOT_EQ,
                Compare.IS,
                Compare.IS_NOT,
            )
        ]
        # a < b <= c or a >= b > c is allowed
        gt_changes = self._code_change_for_comp_permutations((Compare.GT, Compare.GTE))
        lt_changes = self._code_change_for_comp_permutations((Compare.LT, Compare.LTE))
        return same_op_changes + gt_changes + lt_changes

    def _code_change_for_comp_permutations(
        self, comps: typing.Tuple[Compare.Op, ...]
    ) -> typing.List[CodeChange]:
        comp_values = [comp.value for comp in comps]
        return [
            self._code_change_for_comp_pair(left_comp, right_comp)
            for left_comp in comp_values
            for right_comp in comp_values
        ]

    def _code_change_for_comp_pair(
        self, left_comp_value: str, right_comp_value: str
    ) -> CodeChange:
        return CodeChange(
            pattern="${a} "
            + left_comp_value
            + " ${b | not self.writes_any_variables(b)} and ${b} "
            + right_comp_value
            + " ${c}",
            replacement="${a} "
            + left_comp_value
            + " ${b} "
            + right_comp_value
            + " ${c}",
        )

    def description(self) -> str:
        return "Combine two compares on same value into a chained compare"
