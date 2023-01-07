"""Helper fixtures and plugin definitions for pytest
"""

import asyncio
from abc import ABC, abstractmethod
from importlib.metadata import EntryPoint, entry_points
from pathlib import Path
from typing import Any, Generic

import pytest
from cppython_core.plugin_schema.generator import GeneratorGroupData, GeneratorT
from cppython_core.plugin_schema.interface import InterfaceT
from cppython_core.plugin_schema.provider import ProviderGroupData, ProviderT
from cppython_core.plugin_schema.scm import SCMT
from cppython_core.resolution import (
    resolve_cppython_plugin,
    resolve_generator,
    resolve_provider,
)
from cppython_core.schema import (
    CorePluginData,
    CPPythonData,
    CPPythonPluginData,
    DataPluginT,
    PEP621Data,
    PluginGroupDataT,
    PluginT,
    ProjectData,
)

from pytest_cppython.fixtures import CPPythonFixtures


class PluginTests(CPPythonFixtures, ABC, Generic[PluginT]):
    """Shared testing information for all plugin test classes.
    Not subclassed by DataPluginTests to reduce ancestor count
    """

    @abstractmethod
    @pytest.fixture(name="plugin_type", scope="session")
    def fixture_plugin_type(self) -> type[PluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(name="entry_point", scope="session")
    def fixture_entry_point(self, plugin_type: type[PluginT]) -> EntryPoint:
        """Extracts the public entry point information. Guaranteed to exist, because the existence is tested elsewhere

        Args:
            plugin_type: A plugin type

        Return:
            The entry point definition
        """
        (plugin_entry,) = entry_points(group=f"cppython.{plugin_type.group()}")

        return plugin_entry


class PluginIntegrationTests(PluginTests[PluginT]):
    """Integration testing information for all plugin test classes"""


class PluginUnitTests(PluginTests[PluginT]):
    """Unit testing information for all plugin test classes"""


class DataPluginTests(CPPythonFixtures, ABC, Generic[PluginGroupDataT, DataPluginT]):
    """Shared testing information for all data plugin test classes.
    Not inheriting PluginTests to reduce ancestor count
    """

    @abstractmethod
    @pytest.fixture(
        name="plugin_type",
        scope="session",
    )
    def fixture_plugin_type(self) -> type[DataPluginT]:
        """A required testing hook that allows type generation"""

        raise NotImplementedError("Subclasses should override this fixture")

    @pytest.fixture(
        name="cppython_plugin_data",
        scope="session",
    )
    def fixture_cppython_plugin_data(
        self, cppython_data: CPPythonData, plugin_type: type[DataPluginT]
    ) -> CPPythonPluginData:
        """Fixture for created the plugin CPPython table

        Args:
            cppython_data: The CPPython table to help the resolve
            plugin_type: The data plugin type

        Returns:
            The plugin specific CPPython table information
        """

        return resolve_cppython_plugin(cppython_data, plugin_type)

    @pytest.fixture(
        name="core_plugin_data",
        scope="session",
    )
    def fixture_core_plugin_data(
        self, cppython_plugin_data: CPPythonPluginData, project_data: ProjectData, pep621_data: PEP621Data
    ) -> CorePluginData:
        """Fixture for creating the wrapper CoreData type

        Args:
            cppython_plugin_data: CPPython data
            project_data: The project data
            pep621_data: Project table data

        Returns:
            Wrapper Core Type
        """

        return CorePluginData(cppython_data=cppython_plugin_data, project_data=project_data, pep621_data=pep621_data)

    @staticmethod
    @pytest.fixture(
        name="plugin",
        scope="session",
    )
    def fixture_plugin(
        plugin_type: type[DataPluginT],
        entry_point: EntryPoint,
        plugin_group_data: PluginGroupDataT,
        core_plugin_data: CorePluginData,
        plugin_data: dict[str, Any],
    ) -> DataPluginT:
        """Overridden plugin generator for creating a populated data plugin type

        Args:
            plugin_type: Plugin type
            entry_point: Info
            plugin_group_data: The data group configuration
            core_plugin_data: The core metadata
            plugin_data: The data table

        Returns:
            A newly constructed provider
        """

        plugin = plugin_type(entry_point, plugin_group_data, core_plugin_data)

        plugin.activate(plugin_data)

        return plugin


class DataPluginIntegrationTests(
    DataPluginTests[PluginGroupDataT, DataPluginT],
    Generic[PluginGroupDataT, DataPluginT],
):
    """Integration testing information for all data plugin test classes"""


class DataPluginUnitTests(
    DataPluginTests[PluginGroupDataT, DataPluginT],
    Generic[PluginGroupDataT, DataPluginT],
):
    """Unit testing information for all data plugin test classes"""

    def test_empty_activation(self, plugin: DataPluginT) -> None:
        """Data plugins should be able to be defaulted. Sending in empty data is as close to enforcing that behavior
        that we can get

        Args:
            plugin: The data plugin
        """

        plugin.activate({})

    def test_activation(self, plugin: DataPluginT, plugin_data: dict[str, Any]) -> None:
        """Tests activation

        Args:
            plugin: The data plugin
            plugin_data: Data to validate
        """

        plugin.activate(plugin_data)

    def test_pyproject_undefined(self, plugin_data_path: Path | None) -> None:
        """Verifies that the directory data provided by plugins does not contain a pyproject.toml file

        Args:
            plugin_data_path: The plugin's tests/data directory
        """

        if plugin_data_path is not None:
            paths = list(plugin_data_path.rglob("pyproject.toml"))

            assert not paths


class InterfaceTests(PluginTests[InterfaceT]):
    """Shared functionality between the different Interface testing categories"""

    @pytest.fixture(name="plugin")
    def fixture_plugin(
        self,
        plugin_type: type[InterfaceT],
        entry_point: EntryPoint,
    ) -> InterfaceT:
        """Fixture creating the interface.
        Args:
            plugin_type: An input interface type
            entry_point: Setuptools entry information

        Returns:
            A newly constructed interface
        """
        return plugin_type(entry_point)


class InterfaceIntegrationTests(PluginIntegrationTests[InterfaceT], InterfaceTests[InterfaceT], Generic[InterfaceT]):
    """Base class for all interface integration tests that test plugin agnostic behavior"""


class InterfaceUnitTests(PluginUnitTests[InterfaceT], InterfaceTests[InterfaceT], Generic[InterfaceT]):
    """Custom implementations of the Interface class should inherit from this class for its tests.
    Base class for all interface unit tests that test plugin agnostic behavior
    """


class ProviderTests(DataPluginTests[ProviderGroupData, ProviderT], Generic[ProviderT]):
    """Shared functionality between the different Provider testing categories"""

    @pytest.fixture(name="plugin_configuration_type", scope="session")
    def fixture_plugin_configuration_type(self) -> type[ProviderGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return ProviderGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, project_data: ProjectData, cppython_data: CPPythonData) -> ProviderGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            project_data: The workspace configuration
            cppython_data: CPPython data

        Returns:
            The plugin configuration
        """

        return resolve_provider(project_data, cppython_data)


class ProviderIntegrationTests(
    DataPluginIntegrationTests[ProviderGroupData, ProviderT],
    ProviderTests[ProviderT],
    Generic[ProviderT],
):
    """Base class for all provider integration tests that test plugin agnostic behavior"""

    @pytest.fixture(autouse=True, scope="session")
    def _fixture_install_dependency(self, plugin: ProviderT, install_path: Path) -> None:
        """Forces the download to only happen once per test session"""

        path = install_path / plugin.name()
        path.mkdir(parents=True, exist_ok=True)

        asyncio.run(plugin.download_tooling(path))

    def test_install(self, plugin: ProviderT) -> None:
        """Ensure that the vanilla install command functions

        Args:
            plugin: A newly constructed provider
        """
        plugin.install()

    def test_update(self, plugin: ProviderT) -> None:
        """Ensure that the vanilla update command functions

        Args:
            plugin: A newly constructed provider
        """
        plugin.update()


class ProviderUnitTests(
    DataPluginUnitTests[ProviderGroupData, ProviderT],
    ProviderTests[ProviderT],
    Generic[ProviderT],
):
    """Custom implementations of the Provider class should inherit from this class for its tests.
    Base class for all provider unit tests that test plugin agnostic behavior
    """


class GeneratorTests(DataPluginTests[GeneratorGroupData, GeneratorT], Generic[GeneratorT]):
    """Shared functionality between the different Generator testing categories"""

    @pytest.fixture(name="plugin_configuration_type", scope="session")
    def fixture_plugin_configuration_type(self) -> type[GeneratorGroupData]:
        """A required testing hook that allows plugin configuration data generation

        Returns:
            The configuration type
        """

        return GeneratorGroupData

    @pytest.fixture(name="plugin_group_data", scope="session")
    def fixture_plugin_group_data(self, project_data: ProjectData) -> GeneratorGroupData:
        """Generates plugin configuration data generation from environment configuration

        Args:
            project_data: The workspace configuration

        Returns:
            The plugin configuration
        """

        return resolve_generator(project_data)


class GeneratorIntegrationTests(
    DataPluginIntegrationTests[GeneratorGroupData, GeneratorT],
    GeneratorTests[GeneratorT],
    Generic[GeneratorT],
):
    """Base class for all scm integration tests that test plugin agnostic behavior"""


class GeneratorUnitTests(
    DataPluginUnitTests[GeneratorGroupData, GeneratorT],
    GeneratorTests[GeneratorT],
    Generic[GeneratorT],
):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior"""


class SCMTests(
    PluginTests[SCMT],
    Generic[SCMT],
):
    """Shared functionality between the different SCM testing categories"""

    @pytest.fixture(name="plugin")
    def fixture_plugin(
        self,
        plugin_type: type[SCMT],
        entry_point: EntryPoint,
    ) -> SCMT:
        """Fixture creating the plugin.
        Args:
            plugin_type: An input plugin type
            entry_point: Setuptools entry information

        Returns:
            A newly constructed plugin
        """
        return plugin_type(entry_point)


class SCMIntegrationTests(
    PluginIntegrationTests[SCMT],
    SCMTests[SCMT],
    Generic[SCMT],
):
    """Base class for all generator integration tests that test plugin agnostic behavior"""


class SCMUnitTests(
    PluginUnitTests[SCMT],
    SCMTests[SCMT],
    Generic[SCMT],
):
    """Custom implementations of the Generator class should inherit from this class for its tests.
    Base class for all Generator unit tests that test plugin agnostic behavior
    """

    def test_not_repository(self, plugin: SCMT, tmp_path: Path) -> None:
        """Tests that the temporary directory path will not be registered as a repository

        Args:
            plugin: The SCM constructed type
            tmp_path: Temporary directory
        """

        assert not plugin.is_repository(tmp_path)
