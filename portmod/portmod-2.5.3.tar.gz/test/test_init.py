# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Tests the setup systems
"""

import os
import sys
from contextlib import redirect_stdout
from io import StringIO

import pytest

from portmod._cli.main import main
from portmod.config.profiles import get_profile_path
from portmod.globals import env
from portmod.prefix import get_prefixes
from portmod.repos import get_local_repos

from .env import setup_env, setup_no_prefix, tear_down_env


@pytest.fixture(autouse=False)
def setup():
    """
    Sets up test repo for querying
    """
    yield setup_no_prefix()
    tear_down_env()


@pytest.fixture(autouse=False)
def setup_prefix():
    """
    Sets up test repo for querying
    """
    yield setup_env("test")
    tear_down_env()


def test_init_prefix(setup):
    """Tests prefix creation"""
    sys.argv = ["portmod", "init", "test2", "test", "--no-confirm"]
    main()

    assert get_prefixes()["test2"].arch == "test"
    sys.argv = ["portmod", "test2", "destroy", "--no-confirm"]
    main()
    assert "test2" not in get_prefixes()


def test_init_prefix_interactive(setup):
    """Tests prefix creation"""
    env.set_prefix(None)
    sys.argv = ["portmod", "init", "test2", "test"]
    oldstdin = sys.stdin
    # Note: these are hardcoded indices which may change
    # 3 is for the test repository, 0 for the first profile in the list
    # (doesn't matter which one, we're just testing that the profile is selected correctly)

    # The test repository has two copies of the test-extra repository which gets pulled in
    # as repos 1 and 2 to test for a bug where running sync with a prefix set will cause an
    # error when a new repository gets synched twice, as in this case where test-extra and
    # text-extra2 both depend on blank.
    stringio = StringIO("1,2,3\n0\n")
    env.INTERACTIVE = True
    sys.stdin = stringio
    main()
    sys.stdin = oldstdin
    env.INTERACTIVE = False

    env.set_prefix("test2")
    assert os.path.exists(get_profile_path())

    assert get_prefixes()["test2"].arch == "test"
    sys.argv = ["portmod", "test2", "destroy", "--no-confirm"]
    main()
    assert "test2" not in get_prefixes()


def test_add_repo(setup_prefix):
    """Tests adding repositories automatically"""
    stringio = StringIO()
    with redirect_stdout(stringio):
        sys.argv = ["portmod", "test", "select", "repo", "list"]
        main()
    assert "blank" in stringio.getvalue()

    sys.argv = ["portmod", "test", "select", "repo", "add", "blank"]
    main()

    assert any(repo.name == "blank" for repo in env.REPOS)
    assert "blank" in get_local_repos()
