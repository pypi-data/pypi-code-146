"""Identifier Factory."""
from typing import Literal

from whats_this_payload.base import BaseIdentifier
from whats_this_payload.exceptions import NotSupportedWebhookError
from whats_this_payload.whatsapp import WhatsappIdentifier

# @overload
# def get_identifier(webhook: Literal["whatsapp"]) -> Type[WhatsappIdentifier]:
#     ...


def get_identifier(webhook: Literal["whatsapp"]) -> type[BaseIdentifier]:
    """Get the requested indetifier class."""
    if webhook == "whatsapp":
        return WhatsappIdentifier

    raise NotSupportedWebhookError(webhook=webhook)
