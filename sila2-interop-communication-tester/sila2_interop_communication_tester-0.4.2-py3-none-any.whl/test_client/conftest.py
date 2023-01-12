"""Pytest configuration file"""

import grpc
import pytest
from _pytest.python import Class, Function

from sila2_interop_communication_tester import __version__
from sila2_interop_communication_tester.grpc_stubs.SiLABinaryTransfer_pb2_grpc import (
    BinaryDownloadStub,
    BinaryUploadStub,
)
from sila2_interop_communication_tester.helpers.utils import normalize_docstring

# is set in __main__.py
CHANNEL: grpc.Channel = grpc.insecure_channel("127.0.0.1:50052")


@pytest.fixture(scope="session")
def channel() -> grpc.Channel:
    return CHANNEL  # noqa: F821


@pytest.fixture(scope="session")
def binary_download_stub(channel) -> BinaryDownloadStub:
    return BinaryDownloadStub(channel)


@pytest.fixture(scope="session")
def binary_upload_stub(channel) -> BinaryUploadStub:
    return BinaryUploadStub(channel)


@pytest.fixture(scope="session", autouse=True)
def log_global_env_facts(record_testsuite_property):
    record_testsuite_property("version", __version__)


def pytest_collection_modifyitems(session, config, items: list[Function]):
    """Modify test functions"""
    for item in items:  # items: test functions
        if isinstance(item.parent, Class):
            parent = item.parent.newinstance()
        else:
            parent = item.parent.obj
        test_docstring = getattr(parent, item.originalname).__doc__

        if test_docstring:
            item.user_properties.append(("doc", normalize_docstring(test_docstring)))
