"""Tests for vacuum."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import pytest

import mqtt_hass_base.error
from mqtt_hass_base.entity.vacuum import MqttVacuum


class TestEntityVacuum:
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

        mbs = MqttVacuum(
            name="test_vacuum",
            unique_id="test_vacuum",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            supported_features=[],
            fan_speed_list=[],
            object_id="fake_id",
        )

        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)

        with pytest.raises(mqtt_hass_base.error.MQTTHassBaseError):
            await mbs.send_state("BAD_STATE", attributes={"attr1": "value1"})

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

        mbs = MqttVacuum(
            name="test_vacuum",
            unique_id="test_vacuum",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            supported_features=[],
            fan_speed_list=[],
            object_id="fake_id",
            entity_category="config",
        )
        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)

        assert (
            publish_results[f"{self.mqtt_discov_topic}/vacuum/test_vacuum/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/vacuum/test_vacuum/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/vacuum/test_vacuum/availability",
                },
                "command_topic": f"{self.mqtt_data_topic}/vacuum/test_vacuum/command",
                "device": {},
                "fan_speed_list": [],
                "json_attributes_topic": f"{self.mqtt_data_topic}/vacuum/test_vacuum/attributes",
                "name": "test_vacuum",
                "payload_clean_spot": "clean_spot",
                "payload_locate": "locate",
                "payload_pause": "pause",
                "payload_return_to_base": "return_to_base",
                "payload_start": "start",
                "payload_stop": "stop",
                "qos": 0,
                "retain": False,
                "schema": "state",
                "send_command_topic": f"{self.mqtt_data_topic}/vacuum/test_vacuum/send_command",
                "set_fan_speed_topic": f"{self.mqtt_data_topic}/vacuum/test_vacuum/set_fan_speed",
                "state_topic": f"{self.mqtt_data_topic}/vacuum/test_vacuum/state",
                "supported_features": [],
                "unique_id": "test_vacuum",
                "config_object_id": "fake_id",
                "entity_category": "config",
            }
        )

        await mbs.send_state(
            "cleaning", attributes={"attr1": "value1"}, battery_level=50, fan_speed="1"
        )
        assert (
            publish_results[f"{self.mqtt_data_topic}/vacuum/test_vacuum/state"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_data_topic}/vacuum/test_vacuum/state"][
            1
        ] == json.dumps({"state": "cleaning", "battery_level": 50, "fan_speed": "1"})
        assert mbs.state == "cleaning"
        assert publish_results[f"{self.mqtt_data_topic}/vacuum/test_vacuum/attributes"][
            1
        ] == json.dumps({"attr1": "value1"})

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/vacuum/test_vacuum/config"][1]
            is None
        )
