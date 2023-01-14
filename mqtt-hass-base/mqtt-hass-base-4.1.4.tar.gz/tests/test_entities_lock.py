"""Tests for lock."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import pytest

import mqtt_hass_base.error
from mqtt_hass_base.entity.lock import MqttLock


class TestEntityLock:
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

        mbs = MqttLock(
            name="test_lock",
            unique_id="test_lock",
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

        with pytest.raises(mqtt_hass_base.error.MQTTHassBaseError):
            await mbs.send_state("ON", attributes={"attr1": "value1"})

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

        mbs = MqttLock(
            name="test_lock",
            unique_id="test_lock",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            icon="mdi:icon",
            optimistic=True,
            object_id="fake_id",
            entity_category="config",
        )

        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)

        assert (
            publish_results[f"{self.mqtt_discov_topic}/lock/test_lock/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/lock/test_lock/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/lock/test_lock/availability",
                },
                "command_topic": f"{self.mqtt_data_topic}/lock/test_lock/command",
                "device": {},
                "icon": "mdi:icon",
                "json_attributes_topic": f"{self.mqtt_data_topic}/lock/test_lock/attributes",
                "name": "test_lock",
                "optimistic": True,
                "qos": 0,
                "retain": False,
                "state_locked": "LOCKED",
                "state_topic": f"{self.mqtt_data_topic}/lock/test_lock/state",
                "state_unlocked": "UNLOCKED",
                "unique_id": "test_lock",
                "object_id": "fake_id",
                "entity_category": "config",
            }
        )
        await mbs.send_state("LOCK", attributes={"attr1": "value1"})
        assert publish_results[f"{self.mqtt_data_topic}/lock/test_lock/state"] == (
            True,
            "LOCKED",
        )
        assert publish_results[f"{self.mqtt_data_topic}/lock/test_lock/attributes"][
            1
        ] == json.dumps({"attr1": "value1"})
        await mbs.send_locked()
        assert publish_results[f"{self.mqtt_data_topic}/lock/test_lock/state"] == (
            True,
            "LOCKED",
        )
        await mbs.send_unlocked()
        assert publish_results[f"{self.mqtt_data_topic}/lock/test_lock/state"] == (
            True,
            "UNLOCKED",
        )

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/lock/test_lock/config"][1]
            is None
        )
