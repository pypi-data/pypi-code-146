from dataclasses import dataclass

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_from_list() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
        ]
    )
    assert rs == RichSet.from_list([Something(1, "one"), Something(2, "two")])
