"""Data definitions"""

from pathlib import Path

from cppython_core.schema import (
    CPPythonGlobalConfiguration,
    CPPythonLocalConfiguration,
    PEP621Configuration,
    ProjectConfiguration,
)


def _pep621_configuration_list() -> list[PEP621Configuration]:
    """Creates a list of mocked configuration types

    Returns:
        A list of variants to test
    """
    variants = []

    # Default
    variants.append(PEP621Configuration(name="default-test", version="1.0.0"))

    return variants


def _cppython_local_configuration_list() -> list[CPPythonLocalConfiguration]:
    """Mocked list of local configuration data

    Returns:
        A list of variants to test
    """
    variants = []

    # Default
    variants.append(CPPythonLocalConfiguration())

    return variants


def _cppython_global_configuration_list() -> list[CPPythonGlobalConfiguration]:
    """Mocked list of global configuration data

    Returns:
        A list of variants to test
    """
    variants = []

    data = {"current-check": False}

    # Default
    variants.append(CPPythonGlobalConfiguration())

    # Check off
    variants.append(CPPythonGlobalConfiguration(**data))

    return variants


def _project_configuration_list() -> list[ProjectConfiguration]:
    """Mocked list of project configuration data

    Returns:
        A list of variants to test
    """
    variants = []

    # NOTE: pyproject_file will be overridden by fixture

    # Default
    variants.append(ProjectConfiguration(pyproject_file=Path("pyproject.toml"), version="0.1.0"))

    return variants


pep621_variants = _pep621_configuration_list()
cppython_local_variants = _cppython_local_configuration_list()
cppython_global_variants = _cppython_global_configuration_list()
project_variants = _project_configuration_list()
