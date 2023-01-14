"""MQTT Vacuum entity module."""
import asyncio
import json
import logging
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any

import asyncio_mqtt as mqtt

from mqtt_hass_base.entity.common import EntitySettingsType, MqttEntity
from mqtt_hass_base.error import MQTTHassBaseError

# TODO get it from hass
VACUUM_STATES = (
    "cleaning",
    "docked",
    "paused",
    "idle",
    "returning",
    "error",
)


class VacuumSettingsType(
    EntitySettingsType, total=False
):  # pylint: disable=too-few-public-methods
    """Vacuum entity settings dict format."""

    supported_features: list[str]
    fan_speed_list: str | list[str] | None


class MqttVacuum(MqttEntity):
    """MQTT Vacuum entity class."""

    _component = "vacuum"
    _features = (
        "start",
        "stop",
        "pause",
        "return_home",
        "battery",
        "status",
        "locate",
        "clean_spot",
        "fan_speed",
        "send_command",
    )

    def __init__(
        self,
        name: str,
        unique_id: str,
        mqtt_client: mqtt.Client,
        mqtt_discovery_root_topic: str,
        mqtt_data_root_topic: str,
        logger: logging.Logger,
        device_payload: dict[str, str],
        subscriptions: dict[str, Callable[..., Any]],
        supported_features: list[str],
        fan_speed_list: str | list[str] | None,
        object_id: str | None = None,
        entity_category: str | None = None,
    ):
        """Create a new Vacuum entity."""
        MqttEntity.__init__(
            self,
            name,
            unique_id,
            mqtt_client,
            mqtt_discovery_root_topic,
            mqtt_data_root_topic,
            logger,
            device_payload,
            subscriptions,
            object_id=object_id,
            entity_category=entity_category,
        )
        self._supported_features = supported_features
        self._fan_speed_list = fan_speed_list
        self._state: str | bytes | float | int | None = None

    @property
    def state(self) -> str | bytes | float | int | None:
        """Get the current state of the vacuum."""
        return self._state

    @property
    def send_command_topic(self) -> str:
        """Get the MQTT topic where command should be send to."""
        return "/".join(
            (self.mqtt_data_root_topic, self._component, self.name, "send_command")
        ).lower()

    @property
    def set_fan_speed_topic(self) -> str:
        """Return the current fan/suction speed."""
        return "/".join(
            (self.mqtt_data_root_topic, self._component, self.name, "set_fan_speed")
        ).lower()

    async def register(self) -> None:
        """Register the current entity to Hass.

        Using the MQTT discovery feature of Home Assistant.
        """
        config_payload = {
            "availability": {
                "payload_available": "online",
                "payload_not_available": "offline",
                "topic": self.availability_topic,  # required
            },
            "command_topic": self.command_topic,
            "device": self.device_payload,
            "fan_speed_list": self._fan_speed_list,
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "payload_clean_spot": "clean_spot",
            "payload_locate": "locate",
            "payload_pause": "pause",
            "payload_return_to_base": "return_to_base",
            "payload_start": "start",
            "payload_stop": "stop",
            "qos": 0,
            "retain": False,
            "schema": "state",  # static
            "send_command_topic": self.send_command_topic,
            "set_fan_speed_topic": self.set_fan_speed_topic,
            "state_topic": self.state_topic,
            "supported_features": self._supported_features,
            "unique_id": self._unique_id,
        }

        if self._object_id:
            config_payload["config_object_id"] = self.object_id
        if self.entity_category:
            config_payload["entity_category"] = self.entity_category

        self.logger.debug("%s: %s", self.config_topic, json.dumps(config_payload))
        await self._mqtt_client.publish(
            topic=self.config_topic, retain=True, payload=json.dumps(config_payload)
        )

    async def subscribe(self, stack: AsyncExitStack) -> set[asyncio.Task[None]]:
        """Subscribe to all mqtt topics needed."""
        tasks: set[asyncio.Task[None]] = set()
        if on_command_callback := self._subscriptions.get("command_topic"):
            messages = await stack.enter_async_context(
                self._mqtt_client.filtered_messages(self.command_topic)
            )
            tasks.add(
                asyncio.create_task(self._on_messages(messages, on_command_callback))
            )
            # Subscribe to topic(s)
            # 🤔 Note that we subscribe *after* starting the message
            # loggers. Otherwise, we may miss retained messages.
            await self._mqtt_client.subscribe(self.command_topic)

        if on_send_command_callback := self._subscriptions.get("send_command_topic"):
            messages = await stack.enter_async_context(
                self._mqtt_client.filtered_messages(self.send_command_topic)
            )
            tasks.add(
                asyncio.create_task(
                    self._on_messages(messages, on_send_command_callback)
                )
            )
            # Subscribe to topic(s)
            # 🤔 Note that we subscribe *after* starting the message
            # loggers. Otherwise, we may miss retained messages.
            await self._mqtt_client.subscribe(self.send_command_topic)

        if set_fan_speed_callback := self._subscriptions.get("set_fan_speed_topic"):
            messages = await stack.enter_async_context(
                self._mqtt_client.filtered_messages(self.set_fan_speed_topic)
            )
            tasks.add(
                asyncio.create_task(self._on_messages(messages, set_fan_speed_callback))
            )
            # Subscribe to topic(s)
            # 🤔 Note that we subscribe *after* starting the message
            # loggers. Otherwise, we may miss retained messages.
            await self._mqtt_client.subscribe(self.set_fan_speed_topic)

        return tasks

    async def send_state(
        self,
        state: str | bytes | float | int,
        attributes: dict[str, Any] | None = None,
        battery_level: float | None = None,
        fan_speed: str | None = None,
    ) -> None:  # pylint: disable=arguments-differ
        """Send the current state of the vacuum to Hass."""
        if state not in VACUUM_STATES:
            raise MQTTHassBaseError("Bad state {state} not in {VACUUM_STATES}")
        payload: dict[str, Any] = {}
        payload["state"] = state
        self._state = state
        if battery_level:
            payload["battery_level"] = battery_level
        if fan_speed:
            payload["fan_speed"] = fan_speed
        await self._mqtt_client.publish(
            topic=self.state_topic, retain=True, payload=json.dumps(payload)
        )
        await self.send_attributes(attributes)
