"""Tests config.py."""
import inspect

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
import pytest
from pytest import fixture

from bitfount.federated.transport.config import (
    _DEV_MESSAGE_SERVICE_PORT,
    _DEV_MESSAGE_SERVICE_TLS,
    _DEV_MESSAGE_SERVICE_URL,
    _STAGING_MESSAGE_SERVICE_URL,
    PRODUCTION_MESSAGE_SERVICE_URL,
    MessageServiceConfig,
)
from bitfount.federated.transport.protos.messages_pb2_grpc import MessageServiceStub
from tests.utils.helper import unit_test


@unit_test
class TestMessageServiceConfig:
    """Tests for MessageServiceConfig."""

    @fixture
    def test_url(self) -> str:
        """URL for tests."""
        return "not.a.real.url.com"

    def test_ms_config_raises_value_error_if_production_url_and_tls_disabled(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        """Ensure TLS can't be disabled with production hub url."""
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", "production")
        with pytest.raises(ValueError):
            MessageServiceConfig(tls=False)

    def test_ms_config_raises_value_error_if_staging_url_and_tls_disabled(
        self, monkeypatch: MonkeyPatch
    ) -> None:
        """Ensure TLS can't be disabled with staging hub url."""
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", "staging")
        with pytest.raises(ValueError):
            MessageServiceConfig(tls=False)

    def test_ms_config_url_set_on_staging(self, monkeypatch: MonkeyPatch) -> None:
        """Test url correctly set on staging.."""
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", "staging")
        ms_config = MessageServiceConfig()
        assert ms_config.url == _STAGING_MESSAGE_SERVICE_URL

    def test_ms_config_url_set_on_production(self, monkeypatch: MonkeyPatch) -> None:
        """Test url correctly set on production."""
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", "production")
        ms_config = MessageServiceConfig()
        assert ms_config.url == PRODUCTION_MESSAGE_SERVICE_URL

    def test_ms_config_url_set_on_dev(self, monkeypatch: MonkeyPatch) -> None:
        """Test url correctly set on dev."""
        monkeypatch.setenv("BITFOUNT_ENVIRONMENT", "dev")
        ms_config = MessageServiceConfig()
        assert ms_config.url == _DEV_MESSAGE_SERVICE_URL
        assert ms_config.port == _DEV_MESSAGE_SERVICE_PORT
        assert ms_config.tls == _DEV_MESSAGE_SERVICE_TLS

    def test_ms_config_issues_warning_if_tls_disabled_with_custom_url(
        self, caplog: LogCaptureFixture
    ) -> None:
        """Ensure that warning is issued if tls is disabled with non-bitfount URL."""
        MessageServiceConfig(url="custom.ms.url.com", tls=False)

        assert caplog.records[0].levelname == "WARNING"
        assert (
            caplog.records[0].getMessage()
            == "Message service communication without TLS."
        )
        assert caplog.records[1].levelname == "DEBUG"
        assert (
            caplog.records[1].getMessage()
            == "Message service configuration: {'url': 'custom.ms.url.com', 'port': 443, 'tls': False, 'use_local_storage': False}"  # noqa: B950
        )

    async def test_creates_message_service_stub_secure(self, test_url: str) -> None:
        """Tests create_message_service_stub with TLS."""
        ms_config = MessageServiceConfig(tls=False, url=test_url)
        stub = await ms_config.stub
        assert isinstance(stub, MessageServiceStub)

    async def test_creates_message_service_stub_insecure(self, test_url: str) -> None:
        """Tests create_message_service_stub without TLS."""
        ms_config = MessageServiceConfig(tls=True, url=test_url)
        stub = await ms_config.stub
        assert isinstance(stub, MessageServiceStub)

    def test_stub_property_is_async(self, test_url: str) -> None:
        """Tests that the MessageServiceConfig.stub property is async."""
        # Check is property (properties exist on the class)
        assert isinstance(MessageServiceConfig.stub, property)

        # Check property getter is async
        assert inspect.iscoroutinefunction(MessageServiceConfig.stub.fget)
