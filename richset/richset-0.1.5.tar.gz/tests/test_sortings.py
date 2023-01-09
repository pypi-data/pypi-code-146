from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_sorted() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
            Something(2, "two"),
        ]
    )
    assert rs.sorted(key=lambda r: r.id).to_list() == [
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    ]

    assert rs.sorted(key=lambda r: r.name).to_list() == [
        Something(1, "one"),
        Something(3, "three"),
        Something(2, "two"),
    ]

    assert rs.sorted(key=lambda r: r.id, reverse=True).to_list() == [
        Something(3, "three"),
        Something(2, "two"),
        Something(1, "one"),
    ]


def test_richset_reversed() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
            Something(2, "two"),
        ]
    )
    assert rs.reversed().to_list() == [
        Something(2, "two"),
        Something(3, "three"),
        Something(1, "one"),
    ]
