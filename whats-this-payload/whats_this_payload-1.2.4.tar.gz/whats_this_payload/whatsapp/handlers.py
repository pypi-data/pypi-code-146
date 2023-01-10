"""Handler implementation for whatsapp chain of responsability."""


from typing import Union

from whats_this_payload.base import BaseHandler
from whats_this_payload.base.payload_type import BasePayloadType
from whats_this_payload.typing import Payload
from whats_this_payload.whatsapp.enums import PayloadType


class TextMessageHandler(BaseHandler):
    """Handle for text message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for text message."""
        if (
            "referral" not in payload["value"]["messages"][0].keys()
            and payload["value"]["messages"][0].keys()
            >= {"from", "id", "timestamp", "text", "type"}
            and payload["value"]["messages"][0].keys() >= {"text", "type"}
            and payload["value"]["messages"][0]["type"] == "text"
        ):
            return PayloadType.TEXT_MESSAGE
        return super().handle(payload=payload)


class ReactionMessageHandler(BaseHandler):
    """Handle for reaction message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for reaction message."""
        if payload["value"]["messages"][0]["type"] == "reaction":
            return PayloadType.REACTION_MESSAGE
        return super().handle(payload=payload)


class MediaMessageHandler(BaseHandler):
    """Handle for media message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for media message."""
        if payload["value"]["messages"][0]["type"] == "image":
            return PayloadType.MEDIA_MESSAGE
        return super().handle(payload=payload)


class UnkownMessageHandler(BaseHandler):
    """Handler for unkown message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for unkown message."""
        if payload["value"]["messages"][0]["type"] == "unknown":
            return PayloadType.UNKNOWN_MESSAGE
        return super().handle(payload)


class UnsupportedMessageHandler(BaseHandler):
    """Handler for unsupported message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for unkown message."""
        if payload["value"]["messages"][0]["type"] == "unsupported":
            return PayloadType.UNSUPPORTED_MESSAGE
        return super().handle(payload)


class LocationHandler(BaseHandler):
    """Handler for location message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for location message."""
        if "messages" in payload["value"] and payload["value"]["messages"][
            0
        ].keys() >= {"location"}:
            return PayloadType.LOCATION_MESSAGE
        return super().handle(payload)


class ContactHandler(BaseHandler):
    """Handler for contact message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for contact message."""
        if "contacts" in payload["value"]["messages"][0]:
            return PayloadType.CONTACT_MESSAGE
        return super().handle(payload)


class CallbackFromQuickReplyButtonHandler(BaseHandler):
    """Hanlder for callback from quick reply button payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for callback from quick reply buttons."""
        if payload["value"]["messages"][0]["type"] == "button":
            return PayloadType.CALLBACK_FROM_QUICK_REPLY_BUTTON
        return super().handle(payload)


class AnswerFromListMessageHandler(BaseHandler):
    """Handler for answer from list message payload types."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation for answer from list message."""
        if (
            payload["value"]["messages"][0]["type"] == "interactive"
            and payload["value"]["messages"][0]["interactive"]["type"] == "list_reply"
        ):
            return PayloadType.ANSWER_FROM_LIST_MESSAGE
        return super().handle(payload)


class AnswerToReplyButtonHandler(BaseHandler):
    """Handler for answer to reply button message payload."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if (
            payload["value"]["messages"][0]["type"] == "interactive"
            and payload["value"]["messages"][0]["interactive"]["type"] == "button_reply"
        ):
            return PayloadType.ANSWER_TO_REPLY_BUTTON
        return super().handle(payload)


class MessageTriggeredByClickOnAdsHandler(BaseHandler):
    """Handler for message triggered by click on ads payload."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if payload["value"]["messages"][0].keys() >= {"referral"}:
            return PayloadType.MESSAGE_TRIGGERED_BY_CLICK_TO_ADS
        return super().handle(payload)


class ProductInquiryMessageHandler(BaseHandler):
    """Handler for product inquiry message payload type."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if "context" in payload["value"]["messages"][0] and payload["value"][
            "messages"
        ][0]["context"].keys() == {"from", "id", "referred_product"}:
            return PayloadType.PRODUCT_INQUIRY_MESSAGE
        return super().handle(payload)


class OrderMessageHandler(BaseHandler):
    """Handler for order message payload type."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if "order" in payload["value"]["messages"][0]:
            return PayloadType.ORDER_MESSAGE
        return super().handle(payload)


class UserChangedNumberNotification(BaseHandler):
    """Handler for user changed number notification payload type."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if (
            "system" in payload["value"]["messages"][0]
            and payload["value"]["messages"][0]["system"]["type"]
            == "user_changed_number"
        ):
            return PayloadType.USER_CHANGED_NUMBER_NOTIFICATION
        return super().handle(payload)


class StatusMessageSentHandler(BaseHandler):
    """Handler for status message sent payload type."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if payload["value"]["statuses"][0]["status"] == "sent":
            return PayloadType.STATUS_MESSAGE_SENT
        return super().handle(payload)


class StatusMessageDeliveredHandler(BaseHandler):
    """Handler for status message delivered payload type."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if payload["value"]["statuses"][0]["status"] == "delivered":
            return PayloadType.STATUS_MESSAGE_SENT
        return super().handle(payload)


class StatusMessageFailedHandler(BaseHandler):
    """Handler for status message failed payload type."""

    def handle(self, payload: Payload) -> Union[BasePayloadType, None]:
        """Handle implementation."""
        if payload["value"]["statuses"][0]["status"] == "failed":
            return PayloadType.STATUS_MESSAGE_FAILED
        return super().handle(payload)
