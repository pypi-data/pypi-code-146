import typing as t

MeasureOutcome: t.TypeAlias = int | tuple[int, ...]
Indices: t.TypeAlias = int | slice | t.Iterable[int]
