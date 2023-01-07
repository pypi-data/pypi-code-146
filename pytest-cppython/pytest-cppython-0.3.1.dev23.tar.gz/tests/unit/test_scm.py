"""Tests the unit test plugin
"""

from importlib.metadata import EntryPoint
from typing import Any

import pytest

from pytest_cppython.mock.scm import MockSCM
from pytest_cppython.plugin import SCMUnitTests


class TestCPPythonSCM(SCMUnitTests[MockSCM]):
    """The tests for the Mock version control"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> dict[str, Any]:
        """Returns mock data

        Returns:
            An overridden data instance
        """

        return {}

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockSCM]:
        """A required testing hook that allows type generation

        Returns:
            An overridden version control type
        """
        return MockSCM

    @pytest.fixture(name="entry_point", scope="session")
    def fixture_entry_point(self, plugin_type: type[MockSCM]) -> EntryPoint:
        """Override the entry point for the mock object

        Args:
            plugin_type: A plugin type

        Return:
            The entry point definition
        """

        return plugin_type.generate_entry_point()
