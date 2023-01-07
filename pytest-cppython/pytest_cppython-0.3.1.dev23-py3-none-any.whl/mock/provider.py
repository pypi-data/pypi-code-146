"""Mock provider definitions"""


from pathlib import Path
from typing import Any

from cppython_core.plugin_schema.provider import Provider
from cppython_core.schema import SyncDataT

from pytest_cppython.mock.base import MockBase
from pytest_cppython.mock.generator import MockGenerator, MockSyncData


class MockProvider(Provider, MockBase):
    """A mock provider class for behavior testing"""

    downloaded: Path | None = None

    def activate(self, data: dict[str, Any]) -> None:
        pass

    def sync_data(self, generator_sync_data_type: type[SyncDataT]) -> SyncDataT | None:
        """Gathers synchronization data

        Args:
            generator_sync_data_type: The input generator type

        Raises:
            NotSupportedError: If not supported

        Returns:
            The sync data object
        """

        # This is a mock class, so any generator sync type is OK
        match generator_sync_data_type:
            case MockGenerator(generator_sync_data_type):
                return MockSyncData(name=self.name)
            case _:
                return None

    @classmethod
    async def download_tooling(cls, path: Path) -> None:
        cls.downloaded = path

    def install(self) -> None:
        pass

    def update(self) -> None:
        pass
