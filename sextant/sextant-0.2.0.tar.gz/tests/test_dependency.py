"""Tests of the dependency class"""
import pytest
from sextant.dependency import Dependency
from sextant.module import Module

from . import fixtures

bar = Module("bar", "beer", "1.1.0", ["field.hop:2.0"], fixtures)
unicorn = Module("players", "unicorn", "3.1.4", ["bar.beer:1.1"], fixtures)


@pytest.fixture(name="dep")
def dependency():
    """Returns a dependency with a root"""
    return Dependency(bar, Dependency(unicorn, None))


def test_is_compatible(dep):
    """Test if two dependencies are compatible"""
    oldbeer = Module("bar", "beer", "1.0.0", ["field.hop:2.0"], fixtures)
    assert Dependency(oldbeer, None).is_compatible(dep) is False
    assert dep.is_compatible(dep) is True
    assert dep.root.is_compatible(dep) is True


def test_is_equal(dep):
    """Test if two dependencies are equivalent"""
    no_deps = Dependency(bar, None)
    assert dep == no_deps
    assert dep != Dependency(unicorn, bar)


def test_str(dep):
    """Test string representation"""
    assert str(dep) == "bar.beer:1.1.0 (required by players.unicorn:3.1.4)"
