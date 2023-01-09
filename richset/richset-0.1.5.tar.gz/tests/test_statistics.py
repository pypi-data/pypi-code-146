from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_is_empty() -> None:
    assert RichSet.from_list([]).is_empty()
    assert RichSet[str].from_empty().is_empty()
    assert not RichSet.from_list([Something(1, "one")]).is_empty()


def test_richset_is_non_empty() -> None:
    assert RichSet.from_list([]).is_non_empty() is False
    assert RichSet[str].from_empty().is_non_empty() is False
    assert RichSet.from_list([Something(1, "one")]).is_non_empty() is True


def test_richset_size() -> None:
    assert RichSet[str].from_empty().size() == 0
    assert RichSet.from_list([Something(1, "one")]).size() == 1
    assert (
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
            ]
        ).size()
        == 2
    )


def test_richset_count() -> None:
    assert RichSet.from_list([]).count(lambda r: True) == 0
    assert RichSet.from_list([]).count(lambda r: False) == 0
    rs = RichSet.from_list([Something(1, "one"), Something(2, "two")])
    assert rs.count(lambda r: r.id == 1) == 1
    assert rs.count(lambda r: r.id > 0) == 2
    assert (
        RichSet.from_list(
            [
                Something(1, "one"),
                Something(2, "two"),
                Something(3, "three"),
            ]
        ).count(lambda r: r.id % 2 == 0)
        == 1
    )
