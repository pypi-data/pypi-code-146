"""Tests for binary sensor."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import pytest

import mqtt_hass_base.error
from mqtt_hass_base.entity.binarysensor import MqttBinarysensor


class TestEntityBinarySensor:
    """Base test class."""

    mqtt_discov_topic = "discovery_root_topic"
    mqtt_data_topic = "data_root_topic"

    @pytest.mark.asyncio
    async def test_error(self) -> None:
        """Base error test for binary sensor."""
        with pytest.raises(mqtt_hass_base.error.MQTTHassBaseError):
            fake_mqtt_client = MagicMock()
            MqttBinarysensor(
                name="test_sensor",
                unique_id="test_sensor",
                mqtt_client=fake_mqtt_client,
                mqtt_discovery_root_topic=self.mqtt_discov_topic,
                mqtt_data_root_topic=self.mqtt_data_topic,
                logger=logging.getLogger("test_logger"),
                device_payload={},
                subscriptions={},
                device_class="Bad device class",
            )

    @pytest.mark.asyncio
    async def test_base(self) -> None:
        """Base test for binary sensor."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(
            topic: str, retain: bool, payload: dict[Any, Any]
        ) -> None:
            publish_results[topic] = (retain, payload)

        fake_mqtt_client = MagicMock()
        fake_mqtt_client.publish = fake_publish

        mbs = MqttBinarysensor(
            name="test_sensor",
            unique_id="test_sensor",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            device_class="motion",
            icon="mdi:icon",
            off_delay=10,
            object_id="fake_id",
            entity_category="config",
        )
        assert mbs.component_type == "binary_sensor"
        assert mbs.object_id == "fake_id"
        assert mbs.entity_category == "config"
        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)
        assert (
            publish_results[
                f"{self.mqtt_discov_topic}/binary_sensor/test_sensor/config"
            ][0]
            is True
        )
        assert publish_results[
            f"{self.mqtt_discov_topic}/binary_sensor/test_sensor/config"
        ][1] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/binary_sensor/test_sensor/availability",
                },
                "device": {},
                "expire_after": 0,
                "force_update": False,
                "json_attributes_template": "",
                "json_attributes_topic": (
                    f"{self.mqtt_data_topic}/binary_sensor/test_sensor/attributes"
                ),
                "name": "test_sensor",
                "payload_available": "online",
                "payload_not_available": "offline",
                "payload_off": "OFF",
                "payload_on": "ON",
                "qos": 0,
                "state_topic": f"{self.mqtt_data_topic}/binary_sensor/test_sensor/state",
                "unique_id": "test_sensor",
                "device_class": "motion",
                "off_delay": 10,
                "icon": "mdi:icon",
                "object_id": "fake_id",
                "entity_category": "config",
            }
        )
        await mbs.send_state("ON", attributes={"attr1": "value1"})
        assert publish_results[
            f"{self.mqtt_data_topic}/binary_sensor/test_sensor/state"
        ] == (
            True,
            "ON",
        )
        assert publish_results[
            f"{self.mqtt_data_topic}/binary_sensor/test_sensor/attributes"
        ][1] == json.dumps({"attr1": "value1"})
        await mbs.send_off()
        assert publish_results[
            f"{self.mqtt_data_topic}/binary_sensor/test_sensor/state"
        ] == (
            True,
            "OFF",
        )
        await mbs.send_on()
        assert publish_results[
            f"{self.mqtt_data_topic}/binary_sensor/test_sensor/state"
        ] == (
            True,
            "ON",
        )

        await mbs.send_available()
        assert (
            publish_results["data_root_topic/binary_sensor/test_sensor/availability"][1]
            == "online"
        )
        await mbs.send_not_available()
        assert (
            publish_results["data_root_topic/binary_sensor/test_sensor/availability"][1]
            == "offline"
        )

        await mbs.unregister()
        assert (
            publish_results[
                f"{self.mqtt_discov_topic}/binary_sensor/test_sensor/config"
            ][1]
            is None
        )
