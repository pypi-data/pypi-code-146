from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_union() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    assert rs1.union(rs2).to_set() == {
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    }
    assert rs1.union(rs2).to_set() == rs2.union(rs1).to_set()


def test_richset_intersection() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    assert rs1.intersection(rs2).to_set() == {Something(1, "one")}
    assert rs1.intersection(rs2).to_set() == rs2.intersection(rs1).to_set()


def test_richset_difference() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    assert rs1.difference(rs2).to_set() == {Something(2, "two")}
    assert rs2.difference(rs1).to_set() == {Something(3, "three")}


def test_richset_symmetric_difference() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    assert rs1.symmetric_difference(rs2).to_set() == {
        Something(2, "two"),
        Something(3, "three"),
    }
    assert (
        rs1.symmetric_difference(rs2).to_set()
        == rs2.symmetric_difference(rs1).to_set()
    )


def test_richset_is_subset() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    assert rs1.is_subset(rs2)
    assert not rs2.is_subset(rs1)
    assert RichSet[Something].from_empty().is_subset(rs1)
    assert RichSet[Something].from_empty().is_subset(rs2)


def test_richset_is_superset() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
        ]
    )
    assert rs1.is_superset(rs2)
    assert not rs2.is_superset(rs1)
    assert rs1.is_superset(RichSet[Something].from_empty())
    assert rs2.is_superset(RichSet[Something].from_empty())


def test_richset_is_disjoint() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(3, "three"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs3 = RichSet.from_list(
        [
            Something(3, "three"),
            Something(4, "four"),
        ]
    )
    assert not rs1.is_disjoint(rs2)
    assert not rs2.is_disjoint(rs1)
    assert not rs1.is_disjoint(rs3)
    assert not rs3.is_disjoint(rs1)
    assert rs2.is_disjoint(rs3)
    assert rs3.is_disjoint(rs2)

    assert RichSet[Something].from_empty().is_disjoint(rs1)
    assert RichSet[Something].from_empty().is_disjoint(rs2)
    assert RichSet[Something].from_empty().is_disjoint(rs3)

    assert rs1.is_disjoint(RichSet[Something].from_empty())
    assert rs2.is_disjoint(RichSet[Something].from_empty())
    assert rs3.is_disjoint(RichSet[Something].from_empty())


def test_richset_is_equal_as_set() -> None:
    rs1 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs2 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    rs3 = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs1.is_equal_as_set(rs2)
    assert rs2.is_equal_as_set(rs1)
    assert not rs1.is_equal_as_set(rs3)
    assert not rs3.is_equal_as_set(rs1)

    assert not RichSet[Something].from_empty().is_equal_as_set(rs1)
    assert not RichSet[Something].from_empty().is_equal_as_set(rs2)
    assert not RichSet[Something].from_empty().is_equal_as_set(rs3)

    assert not rs1.is_equal_as_set(RichSet[Something].from_empty())
    assert not rs2.is_equal_as_set(RichSet[Something].from_empty())
    assert not rs3.is_equal_as_set(RichSet[Something].from_empty())
