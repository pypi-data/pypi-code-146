"""MQTT Switch entity module."""
import asyncio
import json
import logging
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any

import asyncio_mqtt as mqtt

from mqtt_hass_base.entity.common import EntitySettingsType, MqttEntity


class ButtonSettingsType(
    EntitySettingsType, total=False
):  # pylint: disable=too-few-public-methods
    """Switch entity settings dict format."""

    device_class: str | None
    icon: str | None


class MqttButton(MqttEntity):
    """MQTT Button entity class."""

    _component = "button"

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
        device_class: str | None = None,
        icon: str | None = None,
        object_id: str | None = None,
        entity_category: str | None = None,
    ):
        """Create a new MQTT sensor entity object."""
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
        self._icon = icon
        self._device_class = device_class

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
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "payload_press": "PRESS",
            "qos": 0,
            "retain": False,
            "object_id": self._object_id,
            "unique_id": self._unique_id,
        }

        if self._device_class:
            config_payload["device_class"] = self._device_class
        if self._icon:
            config_payload["icon"] = self._icon
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
        return tasks

    async def send_state(
        self,
        state: str | bytes | float | int,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """Send the current state of the switch to Home Assistant.

        Does nothing, because a button doesn't have a state
        """
