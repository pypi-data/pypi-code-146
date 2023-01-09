# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Depclean tests
"""

import pytest

from portmod.loader import load_all_installed, load_installed_pkg
from portmod.merge import configure, deselect
from portmodlib.atom import Atom

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_depclean(setup):
    """
    Tests that deselected mods are then depcleaned
    """
    configure(["test/test-1.0", "test/test2-1.0"])
    mod = load_installed_pkg(Atom("test/test2"))
    assert mod
    assert mod in load_all_installed()
    deselect(["test/test2"])
    configure([], depclean=True)
    assert not load_installed_pkg(Atom("test/test2"))

    mod = load_installed_pkg(Atom("test/test"))
    assert mod
    assert mod in load_all_installed()
    deselect(["test/test"])
    configure([], depclean=True)
    # Note: test/test is a system mod, so it cannot be removed


def test_noarg_depclean(setup):
    """
    Tests that deselected mods are then depcleaned
    """
    configure(["test/test6-1.0"])
    configure(["test/test6-1.0"], delete=True)
    assert load_installed_pkg(Atom("test/test3"))
    configure([], depclean=True)
    assert not load_installed_pkg(Atom("test/test3"))
