"""Tests for button."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import paho.mqtt.client as paho
import pytest

from mqtt_hass_base.entity.button import MqttButton


class TestEntityButton:
    """Base test class."""

    mqtt_discov_topic = "discovery_root_topic"
    mqtt_data_topic = "data_root_topic"

    @pytest.mark.asyncio
    async def test_error(self) -> None:
        """Base error test."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(
            topic: str, retain: bool, payload: dict[Any, Any]
        ) -> None:
            publish_results[topic] = (retain, payload)

        fake_mqtt_client = MagicMock()
        fake_mqtt_client.publish = fake_publish

        mbs = MqttButton(
            name="test_button",
            unique_id="test_button",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            device_class="update",
            icon="mdi:icon",
        )
        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)
        assert (
            publish_results[f"{self.mqtt_discov_topic}/button/test_button/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/button/test_button/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "data_root_topic/button/test_button/availability",
                },
                "command_topic": "data_root_topic/button/test_button/command",
                "device": {},
                "json_attributes_topic": "data_root_topic/button/test_button/attributes",
                "name": "test_button",
                "payload_press": "PRESS",
                "qos": 0,
                "retain": False,
                "object_id": None,
                "unique_id": "test_button",
                "device_class": "update",
                "icon": "mdi:icon",
            }
        )

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/button/test_button/config"][1]
            is None
        )

    @pytest.mark.asyncio
    async def test_base(self) -> None:
        """Base test."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(topic: str, retain: bool, payload: str) -> None:
            publish_results[topic] = (retain, payload)

        async def fake_subscribe(  # pylint: disable=unused-argument
            stack: AsyncExitStack,
        ) -> None:
            pass

        fake_mqtt_client = MagicMock()
        fake_mqtt_client.publish = fake_publish
        fake_mqtt_client.subscribe = fake_subscribe

        async def on_command(  # pylint: disable=unused-argument
            msg: paho.MQTTMessage,
        ) -> None:
            """Empty callback function."""

        mbs = MqttButton(
            name="test_button",
            unique_id="test_button",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={"command_topic": on_command},
            object_id="fake_id",
            icon="mdi:icon",
            entity_category="config",
        )

        await mbs.register()

        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)

        assert (
            publish_results[f"{self.mqtt_discov_topic}/button/test_button/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/button/test_button/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "data_root_topic/button/test_button/availability",
                },
                "command_topic": "data_root_topic/button/test_button/command",
                "device": {},
                "json_attributes_topic": "data_root_topic/button/test_button/attributes",
                "name": "test_button",
                "payload_press": "PRESS",
                "qos": 0,
                "retain": False,
                "object_id": "fake_id",
                "unique_id": "test_button",
                "icon": "mdi:icon",
                "config_object_id": "fake_id",
                "entity_category": "config",
            }
        )

        await fake_publish("data_root_topic/button/test_button/command", True, "PRESS")

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/button/test_button/config"][1]
            is None
        )
