"""Test factory."""

import pytest

from whats_this_payload.base import BaseIdentifier
from whats_this_payload.exceptions import NotSupportedWebhookError
from whats_this_payload.factory import get_identifier
from whats_this_payload.whatsapp import WhatsappIdentifier


@pytest.mark.parametrize("expected_identifier", [WhatsappIdentifier])
def test_get_identifier(expected_identifier: type[BaseIdentifier]) -> None:
    """Test factored returns expected identifier."""
    identifier = get_identifier(webhook="whatsapp")
    assert identifier is expected_identifier


def test_get_identifier_that_not_exists() -> None:
    """Test when a not supported webhook is requested raises an error."""
    with pytest.raises(NotSupportedWebhookError):
        get_identifier(webhook="i-dont-exists")  # type: ignore[arg-type]
