import os
from contextlib import ExitStack, contextmanager
from typing import Iterator, Mapping, Optional

EnvValue = Optional[str]


def _set_env(key: str, value: EnvValue) -> EnvValue:
    last: EnvValue = os.getenv(key)

    if value is not None:
        os.environ[key] = value
    elif last is not None:
        del os.environ[key]

    return last


@contextmanager
def push_env(key: str, value: EnvValue) -> Iterator[EnvValue]:
    saved = _set_env(key, value)
    try:
        yield saved
    finally:
        _set_env(key, saved)


@contextmanager
def push_envs(envs: Mapping[str, EnvValue]) -> Iterator[EnvValue]:
    with ExitStack() as stack:
        for k, v in envs.items():
            stack.enter_context(push_env(k, v))
        yield
