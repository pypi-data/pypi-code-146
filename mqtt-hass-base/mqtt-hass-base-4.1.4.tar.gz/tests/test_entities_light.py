"""Test for light."""
import json
import logging
from contextlib import AsyncExitStack
from typing import Any
from unittest.mock import MagicMock

import pytest

from mqtt_hass_base.entity.light import MqttLight


class TestEntityLight:
    """Base test class."""

    mqtt_discov_topic = "discovery_root_topic"
    mqtt_data_topic = "data_root_topic"

    @pytest.mark.asyncio
    async def test_base1(self) -> None:
        """Base test 1."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(
            topic: str, retain: bool, payload: dict[Any, Any]
        ) -> None:
            publish_results[topic] = (retain, payload)

        fake_mqtt_client = MagicMock()
        fake_mqtt_client.publish = fake_publish

        mbs = MqttLight(
            name="test_light",
            unique_id="test_light",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            brightness=True,
            brightness_scale=100,
            color_temp=True,
            effect=True,
            effect_list=["effect1"],
            flash_time_long=5,
            flash_time_short=1,
            hs_=True,
            max_mireds=1000,
            min_mireds=100,
            rgb=True,
            white_value=True,
            xy_=True,
            optimistic=True,
        )

        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)
        assert (
            publish_results[f"{self.mqtt_discov_topic}/light/test_light/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/light/test_light/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/light/test_light/availability",
                },
                "brightness": True,
                "color_temp": True,
                "command_topic": f"{self.mqtt_data_topic}/light/test_light/command",
                "device": {},
                "effect": True,
                "hs": True,
                "json_attributes_topic": f"{self.mqtt_data_topic}/light/test_light/attributes",
                "name": "test_light",
                "optimistic": True,
                "qos": 0,
                "retain": False,
                "rgb": True,
                "schema": "json",
                "state_topic": f"{self.mqtt_data_topic}/light/test_light/state",
                "white_value": True,
                "xy": True,
                "unique_id": "test_light",
                "brightness_scale": 100,
                "effect_list": ["effect1"],
                "flash_time_long": 5,
                "flash_time_short": 1,
                "max_mireds": 1000,
                "min_mireds": 100,
            }
        )

        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/light/test_light/config"][1]
            is None
        )

    @pytest.mark.asyncio
    async def test_base2(self) -> None:
        """Base test 2."""
        publish_results: dict[str, Any] = {}

        async def fake_publish(
            topic: str, retain: bool, payload: dict[str, Any]
        ) -> None:
            publish_results[topic] = (retain, payload)

        fake_mqtt_client = MagicMock()
        fake_mqtt_client.publish = fake_publish

        mbs = MqttLight(
            name="test_light",
            unique_id="test_light",
            mqtt_client=fake_mqtt_client,
            mqtt_discovery_root_topic=self.mqtt_discov_topic,
            mqtt_data_root_topic=self.mqtt_data_topic,
            logger=logging.getLogger("test_logger"),
            device_payload={},
            subscriptions={},
            object_id="fake_id",
            entity_category="diagnostic",
            optimistic=False,
        )

        await mbs.register()
        async with AsyncExitStack() as stack:
            await mbs.subscribe(stack)
        assert (
            publish_results[f"{self.mqtt_discov_topic}/light/test_light/config"][0]
            is True
        )
        assert publish_results[f"{self.mqtt_discov_topic}/light/test_light/config"][
            1
        ] == json.dumps(
            {
                "availability": {
                    "payload_available": "online",
                    "payload_not_available": "offline",
                    "topic": f"{self.mqtt_data_topic}/light/test_light/availability",
                },
                "brightness": False,
                "color_temp": False,
                "command_topic": f"{self.mqtt_data_topic}/light/test_light/command",
                "device": {},
                "effect": False,
                "hs": False,
                "json_attributes_topic": f"{self.mqtt_data_topic}/light/test_light/attributes",
                "name": "test_light",
                "optimistic": False,
                "qos": 0,
                "retain": False,
                "rgb": False,
                "schema": "json",
                "state_topic": f"{self.mqtt_data_topic}/light/test_light/state",
                "white_value": False,
                "xy": False,
                "unique_id": "test_light",
                "object_id": "fake_id",
                "entity_category": "diagnostic",
            }
        )
        await mbs.send_state(
            {"brightness": 81, "state": "OFF"}, attributes={"attr1": "value1"}
        )
        assert publish_results[f"{self.mqtt_data_topic}/light/test_light/state"] == (
            True,
            json.dumps({"brightness": 81, "state": "OFF"}),
        )
        assert publish_results[f"{self.mqtt_data_topic}/light/test_light/attributes"][
            1
        ] == json.dumps({"attr1": "value1"})
        await mbs.unregister()
        assert (
            publish_results[f"{self.mqtt_discov_topic}/light/test_light/config"][1]
            is None
        )
