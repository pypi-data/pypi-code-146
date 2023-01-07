"""Tests the integration test plugin
"""

from importlib.metadata import EntryPoint
from typing import Any

import pytest

from pytest_cppython.mock.generator import MockGenerator
from pytest_cppython.plugin import GeneratorIntegrationTests


class TestCPPythonGenerator(GeneratorIntegrationTests[MockGenerator]):
    """The tests for the Mock generator"""

    @pytest.fixture(name="plugin_data", scope="session")
    def fixture_plugin_data(self) -> dict[str, Any]:
        """Returns mock data

        Returns:
            An overridden data instance
        """

        return {}

    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[MockGenerator]:
        """A required testing hook that allows type generation

        Returns:
            An overridden generator type
        """
        return MockGenerator

    @pytest.fixture(name="entry_point", scope="session")
    def fixture_entry_point(self, plugin_type: type[MockGenerator]) -> EntryPoint:
        """Override the entry point for the mock object

        Args:
            plugin_type: A plugin type

        Return:
            The entry point definition
        """

        return plugin_type.generate_entry_point()
