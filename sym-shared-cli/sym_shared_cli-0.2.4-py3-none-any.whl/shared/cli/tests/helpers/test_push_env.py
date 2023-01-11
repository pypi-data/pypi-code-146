from os import environ
from typing import Callable, Iterator
from uuid import UUID

import pytest

from sym.shared.cli.helpers.contexts import push_env


@pytest.fixture
def fresh_env_var(uuid_factory: Callable[[], UUID]) -> Iterator[str]:
    uuid = uuid_factory().hex
    # Extremely unlikely, but just in case:
    while uuid in environ:
        uuid = uuid_factory().hex
    try:
        yield uuid
    finally:
        if uuid in environ:
            del environ[uuid]


def _assert_environ(name: str, value: str) -> None:
    assert environ[name] == value


def _assert_environ_absent(name: str) -> None:
    assert name not in environ


def test_simple(fresh_env_var: str) -> None:
    environ[fresh_env_var] = "foo"
    with push_env(fresh_env_var, "bar"):
        _assert_environ(fresh_env_var, "bar")
    _assert_environ(fresh_env_var, "foo")


def test_from_nil(fresh_env_var: str) -> None:
    with push_env(fresh_env_var, "foo"):
        _assert_environ(fresh_env_var, "foo")
    _assert_environ_absent(fresh_env_var)


def test_to_nil(fresh_env_var: str) -> None:
    environ[fresh_env_var] = "foo"
    with push_env(fresh_env_var, None):
        _assert_environ_absent(fresh_env_var)
    _assert_environ(fresh_env_var, "foo")


def test_from_to_nil(fresh_env_var: str) -> None:
    with push_env(fresh_env_var, None):
        _assert_environ_absent(fresh_env_var)
    _assert_environ_absent(fresh_env_var)
