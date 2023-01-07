"""TODO"""
from importlib.metadata import EntryPoint

from cppython_core.schema import Plugin


class MockBase(Plugin):
    """_summary_"""

    @classmethod
    def generate_entry_point(cls) -> EntryPoint:
        """Generates a mock entry point for this mock class

        Returns:
            The entry point
        """
        return EntryPoint(
            name=f"{cls.name()}",
            value=f"pytest_cppython.mock.scm:{cls.__name__}",
            group=f"cppython.{cls.group()}",
        )
