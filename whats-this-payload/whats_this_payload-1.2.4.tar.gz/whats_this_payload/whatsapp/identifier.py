"""Whatsapp identifier class."""

from whats_this_payload.base import BaseIdentifier
from whats_this_payload.base.payload_type import BasePayloadType
from whats_this_payload.exceptions import NotIdentifiedPayloadError
from whats_this_payload.typing import Payload
from whats_this_payload.utils import build_handler_chain
from whats_this_payload.whatsapp.handlers import (
    AnswerFromListMessageHandler,
    AnswerToReplyButtonHandler,
    CallbackFromQuickReplyButtonHandler,
    ContactHandler,
    LocationHandler,
    MediaMessageHandler,
    MessageTriggeredByClickOnAdsHandler,
    OrderMessageHandler,
    ProductInquiryMessageHandler,
    ReactionMessageHandler,
    StatusMessageDeliveredHandler,
    StatusMessageFailedHandler,
    StatusMessageSentHandler,
    TextMessageHandler,
    UnkownMessageHandler,
    UnsupportedMessageHandler,
    UserChangedNumberNotification,
)


class WhatsappIdentifier(BaseIdentifier):
    """WhatsApp Identifier identifies the payload type of a whatsapp payload."""

    def __init__(self, payload: Payload) -> None:
        """Constructor."""
        self.payload = payload
        self.status_update_handler_chain = build_handler_chain(
            handlers=[
                StatusMessageSentHandler(),
                StatusMessageDeliveredHandler(),
                StatusMessageFailedHandler(),
            ]
        )

        self.interactive_message_handler_chain = build_handler_chain(
            handlers=[
                AnswerFromListMessageHandler(),
                AnswerToReplyButtonHandler(),
            ]
        )
        self.payloads_with_type_handler_chain = build_handler_chain(
            handlers=[
                TextMessageHandler(),
                ReactionMessageHandler(),
                MediaMessageHandler(),
                UnkownMessageHandler(),
                UnsupportedMessageHandler(),
                CallbackFromQuickReplyButtonHandler(),
                MessageTriggeredByClickOnAdsHandler(),
                UserChangedNumberNotification(),
                OrderMessageHandler(),
            ]
        )
        self.product_inquiry_handler_chain = build_handler_chain(
            handlers=[
                ProductInquiryMessageHandler(),
            ]
        )

        self.other_messages_handler_chain = build_handler_chain(
            handlers=[
                ContactHandler(),
                LocationHandler(),
            ]
        )

    def _get_message_changes_from_payload(self) -> Payload:
        return self.payload["entry"][0]["changes"][0]

    def _check_if_payload_changes_has_context(self, payload_changes: Payload) -> bool:
        return bool(payload_changes["value"]["messages"][0].get("context", None))

    def identify_payload_type(self) -> BasePayloadType:
        """Identify payload type from payload."""
        try:
            payload_changes = self._get_message_changes_from_payload()
            if "statuses" in payload_changes["value"]:
                payload_type = self.status_update_handler_chain.handle(
                    payload=payload_changes
                )
            elif "messages" in payload_changes["value"]:

                if (
                    self._check_if_payload_changes_has_context(
                        payload_changes=payload_changes
                    )
                    and "referred_product"
                    in payload_changes["value"]["messages"][0]["context"]
                ):
                    payload_type = self.product_inquiry_handler_chain.handle(
                        payload=payload_changes
                    )
                elif payload_changes["value"]["messages"][0].keys() >= {
                    "interactive",
                }:
                    payload_type = self.interactive_message_handler_chain.handle(
                        payload=payload_changes
                    )
                elif payload_changes["value"]["messages"][0].keys() > {"type"}:
                    payload_type = self.payloads_with_type_handler_chain.handle(
                        payload=payload_changes
                    )
                else:
                    payload_type = self.other_messages_handler_chain.handle(
                        payload=payload_changes
                    )
            else:
                raise NotIdentifiedPayloadError(payload=self.payload)

            if not payload_type:
                raise NotIdentifiedPayloadError(payload=self.payload)
            return payload_type
        except Exception:  # noqa: BLE001
            raise NotIdentifiedPayloadError(payload=self.payload)  # noqa: B904
