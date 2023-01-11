"""Utility functions module"""
# pylint: disable=invalid-name
from typing import TypeVar, Callable
from pathlib import Path
import os

KeyType = TypeVar("KeyType")
EncodedKeyType = TypeVar("EncodedKeyType")
ValueType = TypeVar("ValueType")
ValueFnType = Callable[[KeyType], ValueType]
KeyEncodeFnType = Callable[[KeyType], EncodedKeyType]

try:
    DEFAULT_CACHE_DIR = Path(os.environ["SIMPLE_CACHING_DIR"])
except KeyError:
    # If the env variable is not set, we use the root dir of this project
    DEFAULT_CACHE_DIR = Path(__file__).absolute().parents[1] / ".cache"

def identity_encode_fn(x: KeyType) -> EncodedKeyType:
    """Identity function"""
    return x
