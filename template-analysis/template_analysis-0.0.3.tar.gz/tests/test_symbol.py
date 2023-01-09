from template_analysis.symbol import (
    Symbol,
    SymbolTable,
    SymbolTemplate,
    to_symbol_chunks,
)


def test_to_symbol_chunks() -> None:
    symbol1 = Symbol.create()
    symbol2 = Symbol.create()

    assert to_symbol_chunks(["a", "b", "c"]) == ["abc"]
    assert to_symbol_chunks(["a", "b", symbol1]) == [
        "ab",
        symbol1,
    ]

    assert to_symbol_chunks(["a", "b", symbol1, "c", "d"]) == [
        "ab",
        symbol1,
        "cd",
    ]

    assert to_symbol_chunks([symbol1, "a", "b", symbol2, "c", "d"]) == [
        symbol1,
        "ab",
        symbol2,
        "cd",
    ]


def test_symbol_table() -> None:
    table = SymbolTable.create()
    symbol1 = Symbol.create()
    table.add(symbol1, "a")

    assert table.lookup(symbol1) == "a"
    assert table.lookup("b") == "b"


def test_symbol_template() -> None:
    template = SymbolTemplate([], SymbolTable.create())
    assert template.resolve() == []
    assert template.args() == []

    template = SymbolTemplate(["a", "b", "c"], SymbolTable.create())
    assert template.resolve() == [
        "a",
        "b",
        "c",
    ]
    assert template.args() == []

    table = SymbolTable.create()
    symbol1 = Symbol.create()
    table.add(symbol1, "x")
    template = SymbolTemplate(["a", "b", symbol1, "c", "d"], table)
    assert template.resolve() == ["a", "b", "x", "c", "d"]
    assert template.args() == ["x"]
