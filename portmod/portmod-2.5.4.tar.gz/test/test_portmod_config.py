# Copyright 2019-2021 Portmod Authors
# Distributed under the terms of the GNU General Public License v3

"""
Portmod config tests
"""

import os

import pytest

from portmod.config import get_config, set_config_value
from portmod.globals import env

from .env import setup_env, tear_down_env


@pytest.fixture(scope="module", autouse=True)
def setup():
    """
    Sets up and tears down the test environment
    """
    dictionary = setup_env("test")
    yield dictionary
    tear_down_env()


def test_profile_only_variables(setup):
    """
    Tests that sorting the config files works properly
    """
    get_config()
    with open(env.prefix().CONFIG, "w") as configfile:
        print(
            """
USE_EXPAND = "FOO"
""",
            file=configfile,
        )
    get_config.cache_clear()
    with pytest.raises(UserWarning):
        get_config()

    with open(env.prefix().CONFIG, "w") as configfile:
        print(
            """
ARCH = "BAR"
""",
            file=configfile,
        )

    get_config.cache_clear()
    with pytest.raises(UserWarning):
        get_config()

    with open(env.prefix().CONFIG, "w") as configfile:
        print(
            """
TEST_PROFILE_ONLY = "BAR"
""",
            file=configfile,
        )

    get_config.cache_clear()
    with pytest.raises(UserWarning):
        get_config()


def test_set_config_value():
    def test():
        set_config_value("foo", "1")
        assert get_config()["foo"] == "1"

    # Test with other variable
    with open(env.prefix().CONFIG, "w") as file:
        file.write('bar = "baz"')
    test()

    # Test with just comment
    with open(env.prefix().CONFIG, "w") as file:
        file.write("# Comment")
    test()

    # Test with empty file
    with open(env.prefix().CONFIG, "w"):
        pass
    test()

    # Test with nonexistant file
    os.remove(env.prefix().CONFIG)
    test()
