"""MQTT Light entity module."""
import asyncio
import json
import logging
from collections.abc import Callable
from contextlib import AsyncExitStack
from typing import Any

import asyncio_mqtt as mqtt

from mqtt_hass_base.entity.common import EntitySettingsType, MqttEntity


class LightSettingsType(
    EntitySettingsType, total=False
):  # pylint: disable=too-few-public-methods
    """Light entity settings dict format."""

    optimistic: bool
    brightness: bool
    brightness_scale: int
    color_temp: bool
    effect: bool
    effect_list: list[str] | None
    flash_time_long: int | None
    flash_time_short: int | None
    hs_: bool
    max_mireds: int | None
    min_mireds: int | None
    rgb: bool
    white_value: bool
    xy_: bool


class MqttLight(MqttEntity):
    """MQTT Light entity class."""

    _component = "light"
    _effect_list: list[str] = []

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        unique_id: str,
        mqtt_client: mqtt.Client,
        mqtt_discovery_root_topic: str,
        mqtt_data_root_topic: str,
        logger: logging.Logger,
        device_payload: dict[str, str],
        subscriptions: dict[str, Callable[..., Any]],
        optimistic: bool,
        brightness: bool = False,
        brightness_scale: int = 255,
        color_temp: bool = False,
        effect: bool = False,
        effect_list: list[str] | None = None,
        flash_time_long: int | None = None,
        flash_time_short: int | None = None,
        hs_: bool = False,
        max_mireds: int | None = None,
        min_mireds: int | None = None,
        rgb: bool = False,
        white_value: bool = False,
        xy_: bool = False,
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
        self._brightness = brightness
        self._brightness_scale = brightness_scale
        self._color_temp = color_temp
        self._effect = effect
        if effect_list:
            self._effect_list = effect_list
        self._flash_time_long = flash_time_long
        self._flash_time_short = flash_time_short
        self._hs = hs_
        self._max_mireds = max_mireds
        self._min_mireds = min_mireds
        self._optimistic = optimistic
        self._rgb = rgb
        self._white_value = white_value
        self._xy = xy_

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
            "brightness": self._brightness,
            "color_temp": self._color_temp,
            "command_topic": self.command_topic,
            "device": self.device_payload,
            "effect": self._effect,
            "hs": self._hs,
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            # on_command_type ????
            "optimistic": self._optimistic,
            "qos": 0,
            "retain": False,
            "rgb": self._rgb,
            "schema": "json",
            "state_topic": self.state_topic,
            "white_value": self._white_value,
            "xy": self._xy,
            "unique_id": self._unique_id,
        }

        if self._brightness:
            config_payload["brightness_scale"] = self._brightness_scale
        if self._effect:
            config_payload["effect_list"] = self._effect_list
        if self._flash_time_long:
            config_payload["flash_time_long"] = self._flash_time_long
        if self._flash_time_short:
            config_payload["flash_time_short"] = self._flash_time_short
        if self._max_mireds:
            config_payload["max_mireds"] = self._max_mireds
        if self._min_mireds:
            config_payload["min_mireds"] = self._min_mireds
        if self._object_id:
            config_payload["object_id"] = self.object_id
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
        state: str | bytes | float | int | dict[str, Any],
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """Send the current state of the light to Home Assistant."""
        # TODO validate the state dict
        await self._mqtt_client.publish(
            topic=self.state_topic, retain=True, payload=json.dumps(state)
        )
        await self.send_attributes(attributes)
