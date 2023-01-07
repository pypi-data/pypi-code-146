"""Mock interface definitions"""

from cppython_core.plugin_schema.interface import Interface

from pytest_cppython.mock.base import MockBase


class MockInterface(Interface, MockBase):
    """A mock interface class for behavior testing"""

    def write_pyproject(self) -> None:
        """Implementation of Interface function"""
