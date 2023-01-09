from dataclasses import dataclass

import pytest

from richset import RichSet


@dataclass(frozen=True)
class Something:
    id: int
    name: str


def test_richset_pushed() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.pushed(Something(4, "four")).to_list() == [
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
        Something(4, "four"),
    ]


def test_richset_pushed_all() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.pushed_all([]).to_list() == [
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    ]

    assert rs.pushed_all(
        [
            Something(4, "four"),
            Something(5, "five"),
        ]
    ).to_list() == [
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
        Something(4, "four"),
        Something(5, "five"),
    ]


def test_richset_unshifted() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.unshifted(Something(4, "four")).to_list() == [
        Something(4, "four"),
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    ]


def test_richset_unshifted_all() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.unshifted_all([]).to_list() == [
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    ]

    assert rs.unshifted_all(
        [
            Something(4, "four"),
            Something(5, "five"),
        ]
    ).to_list() == [
        Something(4, "four"),
        Something(5, "five"),
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    ]


def test_richset_popped() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )

    item, rs2 = rs.popped()
    assert item == Something(3, "three")
    assert rs2.to_list() == [
        Something(1, "one"),
        Something(2, "two"),
    ]

    rs = RichSet.from_list([])
    with pytest.raises(IndexError) as err:
        rs.popped()
    assert str(err.value) == "pop from empty RichSet"


def test_richset_popped_n() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )

    popped_items, rs2 = rs.popped_n(2)
    assert popped_items.to_list() == [
        Something(3, "three"),
        Something(2, "two"),
    ]
    assert rs2.to_list() == [Something(1, "one")]

    rs.popped_n(3)
    with pytest.raises(IndexError) as err:
        rs.popped_n(4)
    assert str(err.value) == "pop more than size"

    rs = RichSet.from_list([])
    with pytest.raises(IndexError) as err:
        rs.popped_n(2)
    assert str(err.value) == "pop more than size"


def test_richset_shifted() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )

    item, rs2 = rs.shifted()
    assert item == Something(1, "one")
    assert rs2.to_list() == [
        Something(2, "two"),
        Something(3, "three"),
    ]

    rs = RichSet.from_list([])
    with pytest.raises(IndexError) as err:
        rs.shifted()
    assert str(err.value) == "shift from empty RichSet"


def test_richset_shifted_n() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )

    shifted_items, rs2 = rs.shifted_n(2)
    assert shifted_items.to_list() == [
        Something(1, "one"),
        Something(2, "two"),
    ]
    assert rs2.to_list() == [Something(3, "three")]

    rs.shifted_n(3)
    with pytest.raises(IndexError) as err:
        rs.shifted_n(4)
    assert str(err.value) == "shift more than size"

    rs = RichSet.from_list([])
    with pytest.raises(IndexError) as err:
        rs.shifted_n(2)
    assert str(err.value) == "shift more than size"


def test_richset_slice() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    assert rs.slice(0, 0).to_list() == []
    assert rs.slice(1, 2).to_list() == [Something(2, "two")]
    assert rs.slice(0, 3).to_list() == rs.to_list()
    assert rs.slice(0, 4).to_list() == rs.to_list()
    assert rs.slice(1, 3).to_list() == [
        Something(2, "two"),
        Something(3, "three"),
    ]
    assert rs.slice(-1, 3).to_list() == [Something(3, "three")]


def test_richset_divide_at() -> None:
    rs = RichSet.from_list(
        [
            Something(1, "one"),
            Something(2, "two"),
            Something(3, "three"),
        ]
    )
    rs2, rs3 = rs.divide_at(0)
    assert rs2.to_list() == []
    assert rs3.to_list() == rs.to_list()

    rs2, rs3 = rs.divide_at(1)
    assert rs2.to_list() == [Something(1, "one")]
    assert rs3.to_list() == [Something(2, "two"), Something(3, "three")]

    rs2, rs3 = rs.divide_at(2)
    assert rs2.to_list() == [Something(1, "one"), Something(2, "two")]
    assert rs3.to_list() == [Something(3, "three")]

    rs2, rs3 = rs.divide_at(3)
    assert rs2.to_list() == [
        Something(1, "one"),
        Something(2, "two"),
        Something(3, "three"),
    ]
    assert rs3.to_list() == []
