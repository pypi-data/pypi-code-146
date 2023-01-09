from dataclasses import dataclass

import pytest

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


@dataclass  # not immutable (not hashable)
class SomethingElse:
    id: int
    name: str


def test_richset_from_empty() -> None:
    rs = RichSet[str].from_empty()
    assert rs.is_empty()
    assert not rs.is_non_empty()


def test_richset_from_list() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs == RichSet.from_list([Something(1, "one"), Something(2, "two")])


def test_richset_to_list() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.to_list() == [Something(1, "one"), Something(2, "two")]


def test_richset_from_tuple() -> None:
    rs = RichSet.from_tuple(
        (
            Something(1, "one"),
            Something(2, "two"),
        )
    )
    assert rs.to_list() == [Something(1, "one"), Something(2, "two")]


def test_richset_to_tuple() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.to_tuple() == (Something(1, "one"), Something(2, "two"))


def test_richset_from_set() -> None:
    rs = RichSet.from_set(
        {
            Something(1, "one"),
            Something(2, "two"),
        }
    )
    assert rs.to_set() == {Something(1, "one"), Something(2, "two")}


def test_richset_from_frozenset() -> None:
    rs = RichSet.from_frozenset(
        frozenset(
            {
                Something(1, "one"),
                Something(2, "two"),
            }
        )
    )
    assert rs.to_set() == {Something(1, "one"), Something(2, "two")}


def test_richset_to_set() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.to_set() == {Something(1, "one"), Something(2, "two")}
    assert RichSet[Something].from_empty().to_set() == set({})

    rs2 = RichSet.from_list(
        [
            SomethingElse(1, "one"),
            SomethingElse(2, "two"),
        ]
    )
    with pytest.raises(TypeError) as err:
        rs2.to_set()
    assert "non-hashable record:" in str(err.value)


def test_richset_to_frozenset() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.to_frozenset() == frozenset(
        {Something(1, "one"), Something(2, "two")}
    )
    assert RichSet[Something].from_empty().to_frozenset() == set({})

    rs2 = RichSet.from_list(
        [
            SomethingElse(1, "one"),
            SomethingElse(2, "two"),
        ]
    )
    with pytest.raises(TypeError) as err:
        rs2.to_frozenset()
    assert "non-hashable record:" in str(err.value)


def test_richset_to_dict() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs.to_dict(lambda r: r.id) == {
        1: Something(1, "one"),
        2: Something(2, "two"),
    }

    rs = RichSet.from_list(
        [
            Something(1, "john"),
            Something(2, "jane"),
            Something(3, "john"),  # name duplicated
        ]
    )

    with pytest.raises(ValueError) as err:
        rs.to_dict(lambda r: r.name)
    assert str(err.value) == "duplicate keys"

    with pytest.raises(ValueError) as err:
        rs.to_dict(lambda r: r.name, duplicated="error")
    assert str(err.value) == "duplicate keys"

    assert rs.to_dict(lambda r: r.name, duplicated="first") == {
        "john": Something(1, "john"),
        "jane": Something(2, "jane"),
    }

    assert rs.to_dict(lambda r: r.name, duplicated="last") == {
        "john": Something(3, "john"),
        "jane": Something(2, "jane"),
    }

    # test with a custom duplicate key function
    assert rs.to_dict(
        lambda r: r.name,
        duplicated=lambda items: min(items, key=lambda item: item.id),
    ) == {
        "john": Something(1, "john"),
        "jane": Something(2, "jane"),
    }
    assert rs.to_dict(
        lambda r: r.name,
        duplicated=lambda items: max(items, key=lambda item: item.id),
    ) == {
        "john": Something(3, "john"),
        "jane": Something(2, "jane"),
    }


def test_richset_to_dict_of_list() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "john"),
            Something(2, "jane"),
            Something(3, "john"),  # name duplicated
        ]
    )
    assert rs.to_dict_of_list(lambda r: r.name) == {
        "john": [Something(1, "john"), Something(3, "john")],
        "jane": [Something(2, "jane")],
    }
