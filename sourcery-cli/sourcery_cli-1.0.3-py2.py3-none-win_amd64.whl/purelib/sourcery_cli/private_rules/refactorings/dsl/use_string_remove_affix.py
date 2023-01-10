from typing import List

from lib.version import PythonVersion
from sourcery.conditions.literal_conditions import LiteralConditions
from sourcery.conditions.type_conditions import TypeConditions
from sourcery.dsl.code_change import CodeChange
from sourcery.dsl.proposals import DSLProposer


class UseStringRemoveAffixProposer(DSLProposer, TypeConditions, LiteralConditions):
    def create_code_changes(self) -> List[CodeChange]:
        return [
            CodeChange(
                pattern="""
                    if ${s | has_str_type}.startswith(${const | is_str_literal}):
                        ${s} = ${s}[${length | (
                            self.is_int_literal(length)
                            and length.value == len(const.value)
                        )}:]
                """,
                replacement="""
                    ${s} = ${s}.removeprefix(${const})
                """,
            ),
            CodeChange(
                pattern="""
                    if ${s | has_str_type}.startswith(${t | has_str_type}):
                        ${s} = ${s}[len(${t}):]
                """,
                replacement="""
                    ${s} = ${s}.removeprefix(${t})
                """,
            ),
            CodeChange(
                pattern="""
                    if ${s | has_str_type}.endswith(${const | is_str_literal}):
                        ${s} = ${s}[:${length | (
                            self.is_int_literal(length)
                            and length.value == -len(const.value)
                        )}]
                """,
                replacement="""
                    ${s} = ${s}.removesuffix(${const})
                """,
            ),
            CodeChange(
                pattern="""
                    if ${s | has_str_type}.endswith(${t | has_str_type}):
                        ${s} = ${s}[:-len(${t})]
                """,
                replacement="""
                    ${s} = ${s}.removesuffix(${t})
                """,
            ),
        ]

    def min_python_version(self) -> PythonVersion:
        # https://www.python.org/dev/peps/pep-0616/
        return PythonVersion(major=3, minor=9)

    def description(self) -> str:
        return (
            "Replace a conditional string slice with a call to `str.removesuffix` "
            "or `str.removeprefix`, where applicable"
        )
