"""Tests for MqttClientDevice."""
import asyncio
import logging
from contextlib import AsyncExitStack
from typing import cast

import asyncio_mqtt as mqtt
import paho.mqtt.client as paho
import pytest

from mqtt_hass_base import entity as mqtt_entity
from mqtt_hass_base.device import MqttDevice
from mqtt_hass_base.error import MQTTHassBaseError


class FakeDevice(MqttDevice):
    """Fake mqtt device."""


class TestBase:
    """Base test class."""

    @pytest.mark.asyncio
    async def test_1_main_test(self) -> None:
        """Main test for mqttDevice."""
        async with AsyncExitStack() as stack:
            mqtt_client = mqtt.Client(
                hostname="127.0.0.1",
                port=1883,
                # logger==
                keepalive=60,
                client_id="fake_client",
                username="hass",
                password="hass",
            )

            fake_device = FakeDevice(
                name="fake_device",
                logger=logging.getLogger("root"),
                mqtt_discovery_root_topic="home-assistant",
                mqtt_data_root_topic="fake_device",
                mqtt_client=mqtt_client,
            )

            assert repr(fake_device) == "<FakeDevice 'fake_device'>"

            with pytest.raises(MQTTHassBaseError):
                fake_device.add_entity(
                    "switch",
                    "my_switch",
                    f"{fake_device.name}-my_switch",
                    entity_settings=cast(
                        mqtt_entity.SwitchSettingsType,
                        {"icon": "mdi:icon", "optimistic": False},
                    ),
                    sub_mqtt_topic="fake_device",
                )

            fake_device.name = "new_name"
            fake_device.model = "my_model"
            fake_device.sw_version = "v1"
            fake_device.via_device = "fake_viadevice"
            fake_device.manufacturer = "brand"
            fake_device.mac = "fake_mac"
            assert fake_device.mac == "fake_mac"
            fake_device.add_connections({"ip": "127.0.0.1"})
            fake_device.add_connections(("ip2", "127.0.0.1"))
            with pytest.raises(MQTTHassBaseError):
                fake_device.add_connections(("bad_input", "bad_input", "bad_input"))  # type: ignore
            with pytest.raises(MQTTHassBaseError):
                fake_device.add_connections("bad_input")  # type: ignore
            fake_device.add_identifier("my_id")
            # Test duplication
            assert fake_device.identifiers == ["my_id"]
            fake_device.add_identifier("my_id")
            assert fake_device.identifiers == ["my_id"]
            fake_device.identifiers = ["my_id1", "my_id2"]
            assert fake_device.identifiers == ["my_id1", "my_id2"]
            fake_device.add_identifier("my_id3")
            assert fake_device.identifiers == ["my_id1", "my_id2", "my_id3"]

            callback_messages = []

            async def fake_callback(message: paho.MQTTMessage) -> None:
                callback_messages.append(message.payload)

            with pytest.raises(MQTTHassBaseError):
                fake_device.add_entity(
                    "BAD_TYPE",
                    "my_switch",
                    f"{fake_device.name}-my_switch",
                    entity_settings=cast(
                        mqtt_entity.SwitchSettingsType,
                        {"icon": "mdi:icon", "optimistic": False},
                    ),
                    sub_mqtt_topic="fake_device",
                )

            my_switch = fake_device.add_entity(
                "switch",
                "my_switch",
                f"{fake_device.name}-my_switch",
                entity_settings=cast(
                    mqtt_entity.SwitchSettingsType,
                    {"icon": "mdi:icon", "optimistic": False},
                ),
                subscriptions={"command_topic": fake_callback},
                sub_mqtt_topic="fake_device",
            )

            fake_device.add_entity(
                "light",
                "my_light",
                f"{fake_device.name}-my_light",
                entity_settings=cast(
                    mqtt_entity.LightSettingsType, {"optimistic": False}
                ),
                subscriptions={"command_topic": fake_callback},
            )

            fake_device.add_entity(
                "lock",
                "my_lock",
                f"{fake_device.name}-my_lock",
                entity_settings=cast(
                    mqtt_entity.LockSettingsType,
                    {"icon": "mdi:icon", "optimistic": False},
                ),
                subscriptions={"command_topic": fake_callback},
            )

            fake_device.add_entity(
                "vacuum",
                "my_vacuum",
                f"{fake_device.name}-my_vacuum",
                entity_settings=cast(
                    mqtt_entity.VacuumSettingsType,
                    {
                        "supported_features": [],
                        "fan_speed_list": [],
                    },
                ),
                subscriptions={
                    "command_topic": fake_callback,
                    "send_command_topic": fake_callback,
                    "set_fan_speed_topic": fake_callback,
                },
            )

            assert len(fake_device.entities) == 4

            # tasks: Callable[[Any], Any] = set()
            tasks: set[asyncio.Task[None]] = set()

            await stack.enter_async_context(mqtt_client)
            await asyncio.gather(*tasks)
            fake_device.set_mqtt_client(mqtt_client)
            await fake_device.register()
            await fake_device.subscribe(tasks, stack)
            await fake_device.unregister()

            await mqtt_client.publish(my_switch.command_topic, payload="my_message")
            await asyncio.sleep(1)

        assert callback_messages == [b"my_message"]
