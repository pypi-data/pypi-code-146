from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_group_by() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.group_by(lambda r: r.id % 2)[0] == RichSet.from_list(
        [Something(2, "two")]
    )
    assert rs.group_by(lambda r: r.id % 2)[1] == RichSet.from_list(
        [Something(1, "one"), Something(3, "three")]
    )


def test_richtest_size_of_group_by() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.size_of_group_by(lambda r: r.id % 2)[0] == 1
    assert rs.size_of_group_by(lambda r: r.id % 2)[1] == 2


def test_richset_count_of_group_by() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert (
        rs.count_of_group_by(
            key=lambda r: r.id % 2,
            predicate=lambda x: x.name.startswith("t"),
        )[0]
        == 1
    )
    assert (
        rs.count_of_group_by(
            key=lambda r: r.id % 2,
            predicate=lambda x: x.name.startswith("t"),
        )[1]
        == 1
    )
    assert (
        rs.count_of_group_by(
            key=lambda r: r.id % 2,
            predicate=lambda x: x.name.startswith("o"),
        )[0]
        == 0
    )
    assert (
        rs.count_of_group_by(
            key=lambda r: r.id % 2,
            predicate=lambda x: x.name.startswith("o"),
        )[1]
        == 1
    )


def test_richset_aggregate_by() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.aggregate_by(
        key=lambda r: r.id % 2, fn=lambda a, b: a + b.name, initial=""
    ) == {
        0: "two",
        1: "onethree",
    }
