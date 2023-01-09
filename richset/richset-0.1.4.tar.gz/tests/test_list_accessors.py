from dataclasses import dataclass

import pytest

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_get_first() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.get_first() == Something(1, "one")
    assert rs.get_first(Something(-1, "default")) == Something(1, "one")
    rs2 = RichSet[Something].from_list([])
    assert rs2.get_first() is None
    assert rs2.get_first(Something(-1, "default")) == Something(-1, "default")


def test_richset_first() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.first() == Something(1, "one")

    with pytest.raises(IndexError):
        RichSet.from_list([]).first()


def test_richset_get_last() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.get_last() == Something(2, "two")
    assert rs.get_last(Something(-1, "default")) == Something(2, "two")
    rs2 = RichSet[Something].from_list([])
    assert rs2.get_last() is None
    assert rs2.get_last(Something(-1, "default")) == Something(-1, "default")


def test_richset_last() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.last() == Something(2, "two")

    with pytest.raises(IndexError):
        RichSet.from_list([]).last()


def test_richset_nth() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.nth(0) == Something(1, "one")
    assert rs.nth(1) == Something(2, "two")
    with pytest.raises(IndexError):
        rs.nth(2)

    with pytest.raises(IndexError):
        RichSet.from_list([]).nth(0)


def test_richset_get_nth() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.get_nth(0) == Something(1, "one")
    assert rs.get_nth(1) == Something(2, "two")
    assert rs.get_nth(2, Something(-1, "default")) == Something(-1, "default")
    rs2 = RichSet[Something].from_list([])
    assert rs2.get_nth(0) is None
    assert rs2.get_nth(1, Something(-1, "default")) == Something(-1, "default")


def test_richset_one() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.one() == Something(1, "one")
    with pytest.raises(IndexError) as err:
        RichSet.from_list([]).one()
    assert str(err.value) == "RichSet is empty"


def test_richset_get_one() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.get_one() == Something(1, "one")
    assert rs.get_one(Something(-1, "default")) == Something(1, "one")
    rs2 = RichSet[Something].from_list([])
    assert rs2.get_one() is None
    assert rs2.get_one(Something(-1, "default")) == Something(-1, "default")
