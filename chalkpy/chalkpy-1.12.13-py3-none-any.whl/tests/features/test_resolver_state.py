import dataclasses
from typing import Optional

import pytest

from chalk import State, offline, online
from chalk.features import features


@features
class Acct:
    id: str
    balance: float


@dataclasses.dataclass
class ExplicitDefault:
    cursor: Optional[str]


@dataclasses.dataclass
class ImplicitDefault:
    banana: str = "yellow"
    i: int = 3


@offline
def get_bal(hid: Acct.id, s: State[ImplicitDefault]) -> Acct.balance:
    print(s)
    return 4


@online
def get_bal_2(s: State[ImplicitDefault]) -> Acct.balance:
    print(s)
    return 4


def test_non_constructible_type():
    with pytest.raises(ValueError):

        @online
        def type_non_constructable(s: State[ExplicitDefault]) -> Acct.balance:
            print(s)
            return 4


def test_wrong_default():
    with pytest.raises(ValueError) as e:

        @online
        def wrong_default(s: State[ExplicitDefault] = ImplicitDefault) -> Acct.balance:
            print(s)
            return 4
