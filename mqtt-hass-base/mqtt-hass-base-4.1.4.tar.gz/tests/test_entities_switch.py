"""Tests for switch."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import pytest

import mqtt_hass_base.error
from mqtt_hass_base.entity.switch import MqttSwitch


class TestEntitySwitch:
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

        mbs = MqttSwitch(
            name="test_switch",
            unique_id="test_switch",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            icon="mdi:icon",
            optimistic=True,
        )
        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)
        assert (
            publish_results[f"{self.mqtt_discov_topic}/switch/test_switch/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/switch/test_switch/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/switch/test_switch/availability",
                },
                "command_topic": f"{self.mqtt_data_topic}/switch/test_switch/command",
                "device": {},
                "icon": "mdi:icon",
                "json_attributes_topic": f"{self.mqtt_data_topic}/switch/test_switch/attributes",
                "name": "test_switch",
                "optimistic": True,
                "payload_off": "OFF",
                "payload_on": "ON",
                "qos": 0,
                "retain": False,
                "state_topic": f"{self.mqtt_data_topic}/switch/test_switch/state",
                "object_id": None,
                "unique_id": "test_switch",
            }
        )

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/switch/test_switch/config"][1]
            is None
        )

        with pytest.raises(mqtt_hass_base.error.MQTTHassBaseError):
            await mbs.send_state("BAD STATE", attributes={"attr1": "value1"})

    @pytest.mark.asyncio
    async def test_base(self) -> None:
        """Base test."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(
            topic: str, retain: bool, payload: dict[Any, Any]
        ) -> None:
            publish_results[topic] = (retain, payload)

        fake_mqtt_client = MagicMock()
        fake_mqtt_client.publish = fake_publish

        mbs = MqttSwitch(
            name="test_switch",
            unique_id="test_switch",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            object_id="fake_id",
            icon="mdi:icon",
            optimistic=False,
            entity_category="config",
        )
        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)
        assert (
            publish_results[f"{self.mqtt_discov_topic}/switch/test_switch/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/switch/test_switch/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/switch/test_switch/availability",
                },
                "command_topic": f"{self.mqtt_data_topic}/switch/test_switch/command",
                "device": {},
                "icon": "mdi:icon",
                "json_attributes_topic": f"{self.mqtt_data_topic}/switch/test_switch/attributes",
                "name": "test_switch",
                "optimistic": False,
                "payload_off": "OFF",
                "payload_on": "ON",
                "qos": 0,
                "retain": False,
                "state_topic": f"{self.mqtt_data_topic}/switch/test_switch/state",
                "object_id": "fake_id",
                "unique_id": "test_switch",
                "config_object_id": "fake_id",
                "entity_category": "config",
            }
        )
        await mbs.send_state("ON", attributes={"attr1": "value1"})
        assert publish_results[f"{self.mqtt_data_topic}/switch/test_switch/state"] == (
            True,
            "ON",
        )
        assert publish_results[f"{self.mqtt_data_topic}/switch/test_switch/attributes"][
            1
        ] == json.dumps({"attr1": "value1"})
        await mbs.send_off()
        assert publish_results[f"{self.mqtt_data_topic}/switch/test_switch/state"] == (
            True,
            "OFF",
        )
        await mbs.send_on()
        assert publish_results[f"{self.mqtt_data_topic}/switch/test_switch/state"] == (
            True,
            "ON",
        )

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/switch/test_switch/config"][1]
            is None
        )
