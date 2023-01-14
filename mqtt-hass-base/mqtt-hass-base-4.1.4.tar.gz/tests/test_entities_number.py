"""Tests for number."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import paho.mqtt.client as paho
import pytest

from mqtt_hass_base.entity.number import MqttNumber


class TestEntityNumber:
    """Base test class."""

    mqtt_discov_topic = "discovery_root_topic"
    mqtt_data_topic = "data_root_topic"

    @pytest.mark.asyncio
    async def test_base(self) -> None:
        """Base test."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(
            topic: str, retain: bool, payload: dict[Any, Any]
        ) -> None:
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

        mbs = MqttNumber(
            name="test_number",
            unique_id="test_number",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            min_value=1,
            max_value=10,
            mode="box",
            step=1,
            device_payload={},
            subscriptions={"command_topic": on_command},
            optimistic=True,
            start_value=5,
            payload_reset="RESET",
            object_id="fake_id",
            icon="mdi:icon",
            entity_category="config",
            device_class="temperature",
            unit="C",
        )

        await mbs.register()

        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)

        assert (
            publish_results[f"{self.mqtt_discov_topic}/number/test_number/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/number/test_number/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": "data_root_topic/number/test_number/availability",
                },
                "command_topic": "data_root_topic/number/test_number/command",
                "device": {},
                "icon": "mdi:icon",
                "json_attributes_topic": "data_root_topic/number/test_number/attributes",
                "name": "test_number",
                "optimistic": True,
                "payload_off": "OFF",
                "payload_on": "ON",
                "qos": 0,
                "retain": False,
                "state_topic": "data_root_topic/number/test_number/state",
                "object_id": "fake_id",
                "unique_id": "test_number",
                "min": 1,
                "max": 10,
                "mode": "box",
                "step": 1,
                "device_class": "temperature",
                "payload_reset": "RESET",
                "unit_of_measurement": "C",
                "config_object_id": "fake_id",
                "entity_category": "config",
            }
        )

        await mbs.send_state(33)
        assert publish_results["data_root_topic/number/test_number/state"][1] == 33

        msg = paho.MQTTMessage(1, b"data_root_topic/number/test_number/command")
        msg.payload = b"50"
        await mbs._set_current_value(msg)
        assert mbs.current_value == 50

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/number/test_number/config"][1]
            is None
        )
