"""Test suite for loading modules and managing dependencies."""
import pytest

from sextant import module

from . import fixtures


@pytest.fixture(name="registry")
def fixture_registry():
    """Load the modules in fixtures"""
    return module.registry_from_path(fixtures)


def test_registry_load(registry):
    """Test that loading a module from disc works"""
    assert len(registry.modules) == 10


def test_registry_namespaces(registry):
    """Test that we can correctly identify modules for a namespace."""
    assert len(registry.namespaces) == 3
    assert len(registry.query(namespace="baz")) == 2


def test_registry_query(registry):
    """Test that a query selects modules correctly"""
    assert len(registry.query(namespace="baz")) == 2
    assert len(registry.query(module="beer")) == 2
    assert len(registry.query(version="1.0")) == 6


def test_module_string(registry):
    """Check the string representation of a module."""
    mod = registry.query(module="beer", version="1.0.0").pop()
    assert f"{mod}" == "bar.beer:1.0.0"


def test_module_version_matches(registry):
    """Check version matching between modules"""
    mod = registry.query(module="beer", version="1.0.0").pop()
    for version in ["1.0.0", "1.0", "1"]:
        assert mod.version_matches(version)
    for version in ["1.0.1", "1.1", "2"]:
        assert mod.version_matches(version) is False


def test_module_match(registry):
    """Check a module matches a defined dependency"""
    mod = registry.query(module="beer", version="1.0.0").pop()
    assert mod.matches("bar.beer:1.0")
    assert mod.matches("bar.beer:1.1") is False
    assert mod.matches("baz.beer:1.0") is False


def test_module_newer(registry):
    """Check that a module is newere than another"""
    stools = registry.query(module="stool", version="0.5")
    if stools[0].is_newer(stools[1]):
        assert stools[0].version == "0.5.1"
    else:
        assert stools[0].version == "0.5.0"
    assert stools[0].is_newer(stools[0]) is False
