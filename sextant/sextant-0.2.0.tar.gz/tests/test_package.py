"""Test that packaging works"""
import json
import os
import pathlib
import shutil
import tempfile
from unittest import mock

import pytest

from sextant import dependency, module

from . import fixtures

registry = module.registry_from_path(fixtures)


@pytest.fixture(name="packagefile")
def get_packagefile(request):
    """Create the fake chart directory"""
    try:
        deps = request.param
    except AttributeError:
        deps = ["bar.beer:1.0", "baz.sitting-pangolin:1.0"]

    pkgdir = tempfile.mkdtemp()
    pkgfile = os.path.join(pkgdir, "package.json")
    os.mkdir(os.path.join(pkgdir, "templates"))
    with open(pkgfile, "w", encoding="utf-8") as fhandle:
        json.dump(deps, fhandle)
    yield pkgfile
    shutil.rmtree(pkgdir)


def test_package_init(packagefile):
    """Verify the package initializes correctly"""
    package = dependency.Package(registry, packagefile)
    assert package.lockfile == pathlib.Path(packagefile).parent / "package.lock"
    assert package.modules == ["bar.beer:1.0", "baz.sitting-pangolin:1.0"]


def test_package_lock(packagefile):
    """Verify we can generate a lockfile when a package is correct."""
    package = dependency.Package(registry, packagefile)
    package.lock()
    assert package.lockfile.exists()
    locked_deps = json.loads(package.lockfile.read_bytes())
    for modinfo in [
        {"namespace": "bar", "module": "beer", "version": "1.0.0"},
        {"namespace": "bar", "module": "stool", "version": "0.5.1"},
        {"namespace": "baz", "module": "sitting-pangolin", "version": "1.0.0"},
        {"namespace": "foo", "module": "pangolin", "version": "1.0.0"},
    ]:
        assert modinfo in locked_deps
    # Check the lockfile doesn't get written twice
    package._write_lockfile = mock.MagicMock()
    package.lock()
    package._write_lockfile.assert_not_called()


def test_package_get(packagefile):
    """Verify we can get the contents of the package"""
    package = dependency.Package(registry, packagefile)
    mods = package.get()
    assert registry.query(namespace="foo", module="pangolin", version="1.0.0").pop() in mods


def test_package_get_lockfile(packagefile):
    """Verify we don't recalculate dependencies if a lockfile is present"""
    package = dependency.Package(registry, packagefile)
    package.lock()
    package._fetch_dependencies = mock.MagicMock()
    mods = package.get()
    assert registry.query(namespace="foo", module="pangolin", version="1.0.0").pop() in mods
    package._fetch_dependencies.assert_not_called()


@pytest.mark.parametrize("packagefile", [["baz.drunk-unicorn:1.0", "baz.sitting-pangolin:1.0"]], indirect=True)
def test_package_incompatible_dependencies(packagefile):
    """Verify two incompatible modules cause a dependency error."""
    package = dependency.Package(registry, packagefile)
    with pytest.raises(
        dependency.DependencyError,
        match=r"bar\.beer\:2\.0\.0.*baz\.drunk-unicorn\:1\.0\.0.*bar\.beer\:1\.0\.0.*baz\.sitting-pangolin\:1\.0\.0",
    ):
        package.lock()
