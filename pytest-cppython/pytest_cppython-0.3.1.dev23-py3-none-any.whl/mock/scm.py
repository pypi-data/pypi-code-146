"""Mock SCM definitions"""

from pathlib import Path

from cppython_core.plugin_schema.scm import SCM

from pytest_cppython.mock.base import MockBase


class MockSCM(SCM, MockBase):
    """A mock generator class for behavior testing"""

    def extract_version(self, path: Path) -> str:
        """Extracts the system's version metadata

        Args:
            path: The repository path

        Returns:
            A version
        """
        return "1.0.0"

    def is_repository(self, path: Path) -> bool:
        """Queries repository status of a path

        Args:
            path: The input path to query

        Returns:
            Whether the given path is a repository root
        """
        return False
