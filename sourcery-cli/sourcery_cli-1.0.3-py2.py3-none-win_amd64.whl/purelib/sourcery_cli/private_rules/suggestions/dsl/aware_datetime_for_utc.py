from typing import List

from sourcery.conditions.import_conditions import (
    AddImportPostCondition,
    ImportConditions,
)
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer
from sourcery.engine.rule_type import RuleType


class AwareDatetimeForUtcProposer(DSLProposer, ImportConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    ${dt |
                        self.is_name_node_for_import_name(dt, "datetime.datetime")
                    }.utcnow()
                """,
                replacement="""
                    ${self.node_for_import_name("datetime.datetime")}.now(${
                        self.datetime_timezone().node_for_import_name()
                    }.utc)
                """,
                add_imports_post_condition=self.datetime_timezone(),
                top_level_condition=lambda _: self.has_available_import_name(
                    "datetime.datetime",
                ),
            )
        ]

    def datetime_timezone(self) -> AddImportPostCondition:
        return self.upsert_import("datetime.timezone")

    def description(self) -> str:
        return "Use aware datetime object for UTC"

    def kind(self) -> RuleType:
        return RuleType.SUGGESTION
