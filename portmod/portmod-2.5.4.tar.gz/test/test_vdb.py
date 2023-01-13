# Copyright 2022 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests the mod selection system
"""

import os

import pytest

from portmod.loader import load_pkg
from portmod.package import install_pkg
from portmod.vdb import VDB, vdb_path
from portmodlib.atom import Atom

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup_repo():
    yield setup_env("test")
    tear_down_env()


def test_vdb():
    """
    Tests that all files which need to be installed get added to the package database

    Tests that there are no untracked files in the VDB
    following package installation
    """
    pkg = load_pkg(Atom("test/test-install"))[0]
    install_pkg(pkg, {"foo", "bar"})

    root_path = os.path.join(vdb_path(), "test", "test-install")
    assert os.path.exists(
        os.path.join(root_path, "CONTENTS")
    ), "The CONTENTS file should be present"
    with open(os.path.join(root_path, "CONTENTS")) as file:
        contents = file.readlines()
        assert any(
            os.path.join("pkg", "test", "test-install", "Foo") in line
            for line in contents
        ), "The file installed should be registered in CONTENTS"

    assert os.path.exists(
        os.path.join(root_path, "files", "file")
    ), "The file included in the files directory should be installed"

    assert os.path.exists(
        os.path.join(root_path, "environment.xz")
    ), "The environment file should be installed"

    assert os.path.exists(
        os.path.join(root_path, "Manifest")
    ), "The Manifest file should be installed"

    assert os.path.exists(
        os.path.join(root_path, os.path.basename(pkg.FILE))
    ), "The pybuild file should be installed"

    assert os.path.exists(
        os.path.join(root_path, "REPO")
    ), "The REPO file should be installed"
    with open(os.path.join(root_path, "REPO")) as file:
        assert file.read().strip() == "test", 'The installed REPO should be "test"'

    assert os.path.exists(
        os.path.join(root_path, "USE")
    ), "The USE file should be installed"
    with open(os.path.join(root_path, "USE")) as file:
        assert set(file.read().strip().split()) == {
            "foo",
            "bar",
        }, "The USE flags should be correct"

    with VDB() as vdb:
        assert not vdb.git.ls_files(others=True, exclude_standard=True)
