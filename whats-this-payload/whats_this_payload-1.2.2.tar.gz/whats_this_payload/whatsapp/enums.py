"""Whatsapp enumeration values."""
from whats_this_payload.base.payload_type import BasePayloadType


class PayloadType(BasePayloadType):
    """
    WhatsApp message type enumerations.

    Based on this resource:
    https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples
    """

    # Messages.
    TEXT_MESSAGE = "TEXT_MESSAGE"
    REACTION_MESSAGE = "REACTION_MESSAGE"
    MEDIA_MESSAGE = "MEDIA_MESSAGE"
    UNKNOWN_MESSAGE = "UNKNOWN_MESSAGE"
    LOCATION_MESSAGE = "LOCATION_MESSAGE"
    CONTACT_MESSAGE = "CONTACT_MESSAGE"

    # Replies to interactive components.
    CALLBACK_FROM_QUICK_REPLY_BUTTON = "CALLBACK_FROM_QUICK_REPLY_BUTTON"
    ANSWER_FROM_LIST_MESSAGE = "ANSWER_FROM_LIST_MESSAGE"
    ANSWER_TO_REPLY_BUTTON = "ANSWER_TO_REPLY_BUTTON"
    MESSAGE_TRIGGERED_BY_CLICK_TO_ADS = "MESSAGE_TRIGGERED_BY_CLICK_TO_ADS"

    # Produce inquiry message.
    PRODUCT_INQUIRY_MESSAGE = "PRODUCT_INQUIRY_MESSAGE"

    # Order messages.
    ORDER_MESSAGE = "ORDER_MESSAGE"

    # Notification.
    USER_CHANGED_NUMBER_NOTIFICATION = "USER_CHANGED_NUMBER_NOTIFICATION"

    # Status updates.
    STATUS_MESSAGE_SENT = "STATUS_MESSAGE_SENT"
    STATUS_MESSAGE_DELIVERED = "STATUS_MESSAGE_DELIVERED"
    UNSUPPORTED_MESSAGE = "UNSUPPORTED_MESSAGE"
    STATUS_MESSAGE_FAILED = "MESSAGE_FAILED_STATUS"
