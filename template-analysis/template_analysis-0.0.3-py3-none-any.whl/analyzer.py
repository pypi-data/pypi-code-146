from __future__ import annotations

import difflib
from dataclasses import dataclass
from typing import Union

from .symbol import (
    Chunks,
    Symbol,
    SymbolChunks,
    SymbolString,
    SymbolTable,
    SymbolTemplate,
    to_symbol_chunks,
)
from .template import Template


@dataclass(frozen=True)
class AnalyzerResult:
    text: SymbolString
    tables: list[SymbolTable]

    @property
    def template(self) -> Template:
        return Template.from_symbol_template(
            SymbolTemplate(self.text[:], SymbolTable.create())
        )

    @property
    def args(self) -> list[Chunks]:
        return [
            SymbolTemplate(self.text[:], table).args() for table in self.tables
        ]

    def to_format_string(self) -> str:
        return self.template.to_format_string()

    @classmethod
    def from_text(cls, text: str) -> AnalyzerResult:
        return AnalyzerResult(
            text=list(text),
            tables=[SymbolTable.create()],
        )


@dataclass
class Analyzer:
    text: SymbolString
    pos: int
    parsed: SymbolChunks
    table: SymbolTable

    @classmethod
    def create(cls, text: Union[str, SymbolString]) -> Analyzer:
        return cls(
            list(text),
            pos=0,
            parsed=[],
            table=SymbolTable.create(),
        )

    def proceed(self, size: int) -> None:
        self.pos += size

    @property
    def parsed_text(self) -> SymbolString:
        chunks: SymbolString = []
        for chunk in self.parsed:
            if isinstance(chunk, Symbol):
                chunks.append(chunk)
            else:
                for char in chunk:
                    chunks.append(char)
        return chunks

    def append_match(self, size: int) -> None:
        start = self.pos
        stop = self.pos + size
        token: SymbolString = self.text[start:stop]
        for s in to_symbol_chunks(token):
            if isinstance(s, Symbol):
                self.proceed(1)
            else:
                self.proceed(len(s))
            self.parsed.append(s)

    def append_unique(self, size: int, symbol: Symbol) -> None:
        start = self.pos
        stop = self.pos + size
        token: SymbolString = self.text[start:stop]
        for s in to_symbol_chunks(token):
            if isinstance(s, Symbol):
                self.proceed(1)
            else:
                self.proceed(len(s))
            self.parsed.append(symbol)
            self.table.add(symbol, s)

    def advance(self, pos: int, size: int, symbol: Symbol) -> None:
        while (unmatch_length := pos - self.pos) > 0:
            self.append_unique(unmatch_length, symbol)
        self.append_match(size)

    @classmethod
    def analyze_two_symbol_strings(
        cls, seq1: SymbolString, seq2: SymbolString
    ) -> tuple[Analyzer, Analyzer]:
        matcher = difflib.SequenceMatcher(None, seq1, seq2)
        blocks = matcher.get_matching_blocks()
        analyzer_a = cls.create(seq1)
        analyzer_b = cls.create(seq2)

        for block in blocks:
            symbol = Symbol.create()
            analyzer_a.advance(block.a, block.size, symbol)
            analyzer_b.advance(block.b, block.size, symbol)

        return analyzer_a, analyzer_b

    @classmethod
    def analyze(cls, texts: list[str]) -> AnalyzerResult:
        return cls.analyze_texts(texts)

    @classmethod
    def analyze_two_result(
        cls, result1: AnalyzerResult, result2: AnalyzerResult
    ) -> AnalyzerResult:
        analyzer_a, analyzer_b = cls.analyze_two_symbol_strings(
            result1.text, result2.text
        )
        assert analyzer_a.parsed_text == analyzer_b.parsed_text
        return AnalyzerResult(
            analyzer_a.parsed_text,
            [
                *[
                    analyzer_a.table.combined(table)
                    for table in result1.tables
                ],
                *[
                    analyzer_b.table.combined(table)
                    for table in result2.tables
                ],
            ],
        )

    @classmethod
    def analyze_texts(cls, texts: list[str]) -> AnalyzerResult:
        texts = texts[:]

        if not texts:
            raise ValueError("texts are empty.")

        text = texts.pop(0)
        acc = AnalyzerResult.from_text(text)
        while texts:
            text = texts.pop(0)
            curr = AnalyzerResult.from_text(text)
            acc = cls.analyze_two_result(acc, curr)

        return acc


analyze = Analyzer.analyze
