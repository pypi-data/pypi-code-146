from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_index_of() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
            Something(4, "four"),
            Something(5, "five"),
        ]
    )
    assert rs.index_of(lambda r: r.id == 1) == 0
    assert rs.index_of(lambda r: r.id == 2) == 1
    assert rs.index_of(lambda r: r.id == 6) == -1
    assert rs.index_of(lambda r: r.id % 2 == 0) == 1
    assert rs.index_of(lambda r: r.id % 2 == 1) == 0
    assert rs.index_of(lambda r: r.id == 10) == -1

    assert rs.index_of(lambda r: r.id == 1, reverse=False) == 0
    assert rs.index_of(lambda r: r.id == 2, reverse=False) == 1
    assert rs.index_of(lambda r: r.id == 6, reverse=False) == -1
    assert rs.index_of(lambda r: r.id % 2 == 0, reverse=False) == 1
    assert rs.index_of(lambda r: r.id % 2 == 1, reverse=False) == 0
    assert rs.index_of(lambda r: r.id == 10, reverse=False) == -1

    assert rs.index_of(lambda r: r.id == 1, reverse=True) == 0
    assert rs.index_of(lambda r: r.id == 2, reverse=True) == 1
    assert rs.index_of(lambda r: r.id == 6, reverse=True) == -1
    assert rs.index_of(lambda r: r.id % 2 == 0, reverse=True) == 3
    assert rs.index_of(lambda r: r.id % 2 == 1, reverse=True) == 4
    assert rs.index_of(lambda r: r.id == 10, reverse=True) == -1


def test_richset_indices() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.indices_of(lambda r: r.id == 1) == [0]
    assert rs.indices_of(lambda r: r.id == 2) == [1]
    assert rs.indices_of(lambda r: r.id == 3) == []


def test_richset_search_first() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.search_first(lambda r: r.id == 0) == (-1, None)
    assert rs.search_first(lambda r: r.id == 1) == (0, Something(1, "one"))
    assert rs.search_first(lambda r: r.id == 2) == (1, Something(2, "two"))
    assert rs.search_first(lambda r: r.id == 3) == (2, Something(3, "three"))
    assert rs.search_first(lambda r: r.id > 1) == (1, Something(2, "two"))


def test_richset_search_last() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.search_last(lambda r: r.id == 0) == (-1, None)
    assert rs.search_last(lambda r: r.id == 1) == (0, Something(1, "one"))
    assert rs.search_last(lambda r: r.id == 2) == (1, Something(2, "two"))
    assert rs.search_last(lambda r: r.id == 3) == (2, Something(3, "three"))
    assert rs.search_last(lambda r: r.id > 1) == (2, Something(3, "three"))


def test_richset_search_all() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.search_all(lambda r: r.id == 0) == []
    assert rs.search_all(lambda r: r.id == 1) == [(0, Something(1, "one"))]
    assert rs.search_all(lambda r: r.id == 2) == [(1, Something(2, "two"))]
    assert rs.search_all(lambda r: r.id > 1) == [
        (1, Something(2, "two")),
        (2, Something(3, "three")),
    ]
