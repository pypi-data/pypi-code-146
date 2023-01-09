from __future__ import annotations

from dataclasses import dataclass
from typing import Union

from .symbol import Symbol, SymbolTemplate


@dataclass(frozen=True)
class Variable:
    id: int

    def to_format_string(self) -> str:
        return "{}"


@dataclass(frozen=True)
class PlainText:
    value: str

    def to_format_string(self) -> str:
        return self.value


TemplatePart = Union[PlainText, Variable]


@dataclass(frozen=True)
class Template:
    parts: list[TemplatePart]

    @classmethod
    def from_symbol_template(cls, st: SymbolTemplate) -> Template:
        parts: list[TemplatePart] = []
        variables = 0
        for chunk in st.text:
            if isinstance(chunk, Symbol):
                parts.append(Variable(variables))
                variables += 1
            else:
                parts.append(PlainText(chunk))
        return cls(parts)

    def to_format_string(self) -> str:
        return "".join(part.to_format_string() for part in self.parts)
