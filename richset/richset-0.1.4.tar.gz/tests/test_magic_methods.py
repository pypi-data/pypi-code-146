from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_iter() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    for i, r in enumerate(rs):
        if i == 0:
            assert r == Something(1, "one")
        elif i == 1:
            assert r == Something(2, "two")


def test_richset_len() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert len(rs) == 2
    assert len(RichSet[str].from_empty()) == 0
