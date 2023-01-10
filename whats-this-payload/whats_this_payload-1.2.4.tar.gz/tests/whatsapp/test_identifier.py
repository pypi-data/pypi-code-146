"""Unittesting for Whatsapp Identifier."""

import json
import pathlib

import pytest

from whats_this_payload.exceptions import NotIdentifiedPayloadError
from whats_this_payload.whatsapp import WhatsappIdentifier
from whats_this_payload.whatsapp.enums import PayloadType

CWD = pathlib.Path().cwd()


class TestWhatsappIdentifier:
    """Definition of tests for Whatsapp identifier."""

    @pytest.mark.parametrize(
        ("path_to_payload", "expected_type"),
        [
            (
                (CWD / "tests" / "payload_samples" / "whatsapp" / "text_message.json"),
                PayloadType.TEXT_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "reaction_message.json"
                ),
                PayloadType.REACTION_MESSAGE,
            ),
            (
                (CWD / "tests" / "payload_samples" / "whatsapp" / "media_message.json"),
                PayloadType.MEDIA_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "unkown_message.json"
                ),
                PayloadType.UNKNOWN_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "location_message.json"
                ),
                PayloadType.LOCATION_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "contact_message.json"
                ),
                PayloadType.CONTACT_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "answer_from_list_message.json"
                ),
                PayloadType.ANSWER_FROM_LIST_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "answer_to_reply_button.json"
                ),
                PayloadType.ANSWER_TO_REPLY_BUTTON,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "callback_from_quick_reply_button.json"
                ),
                PayloadType.CALLBACK_FROM_QUICK_REPLY_BUTTON,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "message_triggered_by_click_to_ads.json"
                ),
                PayloadType.MESSAGE_TRIGGERED_BY_CLICK_TO_ADS,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "product_inquiry_message.json"
                ),
                PayloadType.PRODUCT_INQUIRY_MESSAGE,
            ),
            (
                (CWD / "tests" / "payload_samples" / "whatsapp" / "order_message.json"),
                PayloadType.ORDER_MESSAGE,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "user_changed_number_notification.json"
                ),
                PayloadType.USER_CHANGED_NUMBER_NOTIFICATION,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_sent_business_initiated.json"
                ),
                PayloadType.STATUS_MESSAGE_SENT,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_sent_user_initiated_free.json"
                ),
                PayloadType.STATUS_MESSAGE_SENT,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_sent_user_initiated_no_free.json"
                ),
                PayloadType.STATUS_MESSAGE_SENT,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_delivered_business_initiated.json"
                ),
                PayloadType.STATUS_MESSAGE_SENT,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_delivered_user_initiated_free.json"
                ),
                PayloadType.STATUS_MESSAGE_SENT,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_delivered_user_initiated_no_free.json"
                ),
                PayloadType.STATUS_MESSAGE_SENT,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_failed.json"
                ),
                PayloadType.STATUS_MESSAGE_FAILED,
            ),
            (
                (
                    CWD
                    / "tests"
                    / "payload_samples"
                    / "whatsapp"
                    / "status_message_deleted.json"
                ),
                PayloadType.UNSUPPORTED_MESSAGE,
            ),
        ],
    )
    def test_indentify_payload_type(
        self, path_to_payload: pathlib.Path, expected_type: PayloadType
    ) -> None:
        """Test method works correctly."""
        identifier = WhatsappIdentifier(payload=json.loads(path_to_payload.read_text()))
        payload_type = identifier.identify_payload_type()
        assert payload_type == expected_type

    @pytest.mark.parametrize(
        "path_to_payload",
        [
            (CWD / "tests" / "payload_samples" / "not_identifiable.json"),
        ],
    )
    def test_not_identify_payload_type(self, path_to_payload: pathlib.Path) -> None:
        """Test method to check not identified error is raised."""
        identifier = WhatsappIdentifier(payload=json.loads(path_to_payload.read_text()))
        with pytest.raises(NotIdentifiedPayloadError):
            identifier.identify_payload_type()
