import dataclasses
from typing import Optional

import pytest

from chalk import State, offline, online
from chalk.features import features, owner


@features
class Txn:
    id: str
    amount: float


def test_can_define_owner():
    @online(owner="andy@chalk.ai")
    def resolver_with_owner(id: Txn.id) -> Txn.amount:
        ...


def test_can_extract_resolver_owner():
    @online(owner="andy@chalk.ai")
    def resolver_with_owner_2(id: Txn.id) -> Txn.amount:
        ...

    assert owner(resolver_with_owner_2) == "andy@chalk.ai"
