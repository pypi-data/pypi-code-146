"""MQTT Switch entity module."""
import asyncio
import json
import logging
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any, Literal

import asyncio_mqtt as mqtt
import paho.mqtt.client as paho

from mqtt_hass_base.entity.common import EntitySettingsType, MqttEntity


class NumberSettingsType(
    EntitySettingsType, total=False
):  # pylint: disable=too-few-public-methods
    """Switch entity settings dict format."""

    min_value: float
    max_value: float
    step: float
    mode: Literal["auto", "box", "slider"]
    payload_reset: str | None
    unit: str | None
    icon: str | None
    optimistic: bool
    start_value: float | None


class MqttNumber(MqttEntity):
    """MQTT Number entity class."""

    _component = "number"

    def __init__(
        self,
        name: str,
        unique_id: str,
        mqtt_client: mqtt.Client,
        mqtt_discovery_root_topic: str,
        mqtt_data_root_topic: str,
        logger: logging.Logger,
        min_value: float,
        max_value: float,
        mode: Literal["auto", "box", "slider"],
        step: float,
        device_payload: dict[str, str],
        subscriptions: dict[str, Callable[..., Any]],
        optimistic: bool,
        start_value: float | None = None,
        payload_reset: str | None = None,
        unit: str | None = None,
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
        self._optimistic = optimistic
        self._min_value = min_value
        self._max_value = max_value
        self._mode = mode
        self._unit = unit
        self._step = step
        self._payload_reset = payload_reset
        self._start_value = start_value
        self._current_value: float | None = None

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
            "icon": self._icon,
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "optimistic": self._optimistic,
            "payload_off": "OFF",
            "payload_on": "ON",
            "qos": 0,
            "retain": False,
            "state_topic": self.state_topic,
            "object_id": self._object_id,
            "unique_id": self._unique_id,
            "min": self._min_value,
            "max": self._max_value,
            "mode": self._mode,
            "step": self._step,
        }

        if self._device_class:
            config_payload["device_class"] = self._device_class
        if self._payload_reset:
            config_payload["payload_reset"] = self._payload_reset
        if self._unit:
            config_payload["unit_of_measurement"] = self._unit
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
        if self._start_value:
            await self.send_state(self._start_value)
            self._current_value = self._start_value

    async def subscribe(self, stack: AsyncExitStack) -> set[asyncio.Task[None]]:
        """Subscribe to all mqtt topics needed."""
        tasks: set[asyncio.Task[None]] = set()
        if self._subscriptions.get("command_topic"):
            messages = await stack.enter_async_context(
                self._mqtt_client.filtered_messages(self.command_topic)
            )
            tasks.add(
                asyncio.create_task(
                    self._on_messages(messages, self._set_current_value)
                )
            )
            # Subscribe to topic(s)
            # 🤔 Note that we subscribe *after* starting the message
            # loggers. Otherwise, we may miss retained messages.
            await self._mqtt_client.subscribe(self.command_topic)
        return tasks

    async def _set_current_value(self, msg: paho.MQTTMessage) -> None:
        """Save the new current value."""
        # We send back immediatly the new value to the state topic
        await self.send_state(float(msg.payload.decode()))
        if on_command_callback := self._subscriptions.get("command_topic"):
            await on_command_callback(msg)

    @property
    def current_value(self) -> float | None:
        """Get the current value of the entity."""
        return self._current_value

    async def send_state(
        self,
        state: str | bytes | float | int,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """Send the current state of the switch to Home Assistant."""
        self._current_value = float(state)
        await self._mqtt_client.publish(
            topic=self.state_topic,
            retain=True,
            payload=state,
        )
        await self.send_attributes(attributes)
