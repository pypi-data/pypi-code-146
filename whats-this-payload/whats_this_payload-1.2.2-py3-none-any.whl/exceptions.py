"""Customed defined exceptions."""


from whats_this_payload.typing import Payload


class NotIdentifiedPayloadError(Exception):
    """Raised when a payload couldn't been identified."""

    def __init__(self, payload: Payload) -> None:
        """Constructor."""
        super().__init__(
            "payload=`{payload}` couldn't been identified.".format(payload=payload)
        )


class NotSupportedWebhookError(Exception):
    """Raised when a requested identifier is not supported."""

    def __init__(self, webhook: str) -> None:
        """Constructor."""
        super().__init__(
            "Webhook {webhook} is not supported yet.".format(webhook=webhook)
        )
