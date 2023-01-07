"""Shared definitions for testing.
"""

from typing import Any

from cppython_core.plugin_schema.generator import Generator
from cppython_core.schema import SyncData

from pytest_cppython.mock.base import MockBase


class MockSyncData(SyncData):
    """A Mock data type"""


class MockGenerator(Generator[MockSyncData], MockBase):
    """A mock generator class for behavior testing"""

    def activate(self, data: dict[str, Any]) -> None:
        pass

    @staticmethod
    def sync_data_type() -> type[MockSyncData]:
        """_summary_

        Raises:
            NotImplementedError: _description_

        Returns:
            _description_
        """
        return MockSyncData

    def sync(self, sync_data: list[MockSyncData]) -> None:
        """Synchronizes generator files and state with the providers input

        Args:
            sync_data: List of information gathered from providers
        """
