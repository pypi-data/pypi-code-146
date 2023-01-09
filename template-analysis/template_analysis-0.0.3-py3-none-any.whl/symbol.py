from __future__ import annotations

from dataclasses import dataclass
from typing import Union

Character = str
Chunk = str


@dataclass(frozen=True)
class Symbol:
    value: object

    @classmethod
    def create(cls) -> Symbol:
        return cls(object())


@dataclass
class SymbolTable:
    table: dict[Symbol, SymbolChunk]

    @classmethod
    def create(cls) -> SymbolTable:
        return cls({})

    def add(self, symbol: Symbol, chunk: SymbolChunk) -> None:
        self.table[symbol] = chunk

    def lookup(self, symbol_or_chunk: SymbolChunk) -> Chunk:
        while isinstance(symbol_or_chunk, Symbol):
            symbol_or_chunk = self.table[symbol_or_chunk]
        assert isinstance(symbol_or_chunk, Chunk)
        return symbol_or_chunk

    def combined(self, other: SymbolTable) -> SymbolTable:
        new_table = self.table.copy()
        new_table.update(other.table)
        return SymbolTable(new_table)


SymbolOrCharacter = Union[Symbol, Character]
SymbolChunk = Union[Symbol, Chunk]
Chunks = list[Chunk]
SymbolString = list[SymbolOrCharacter]
SymbolChunks = list[SymbolChunk]


def to_symbol_chunks(
    symbol_string: SymbolString,
) -> SymbolChunks:
    x: SymbolChunks = []
    chunk: str = ""
    for symbol_or_character in symbol_string:
        if isinstance(symbol_or_character, Symbol):
            if chunk:
                x.append(chunk)
                chunk = ""
            x.append(symbol_or_character)
        else:
            chunk += symbol_or_character
    if chunk:
        x.append(chunk)
    return x


@dataclass(frozen=True)
class SymbolTemplate:
    text: SymbolChunks
    table: SymbolTable

    def resolve(self) -> Chunks:
        return [self.table.lookup(chunk) for chunk in self.text]

    def args(self) -> list[Chunk]:
        return [
            self.table.lookup(chunk)
            for chunk in self.text
            if isinstance(chunk, Symbol)
        ]
