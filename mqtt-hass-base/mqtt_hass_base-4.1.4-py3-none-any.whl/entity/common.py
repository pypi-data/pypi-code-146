"""MQTT base entity module."""
import asyncio
import json
import logging
from collections.abc import AsyncGenerator, Callable
from contextlib import AsyncExitStack
from typing import Any, TypedDict

import asyncio_mqtt as mqtt
import paho.mqtt.client as paho

from mqtt_hass_base.error import MQTTHassBaseError

# TODO: python 3.11 => uncomment NotRequired
# from typing_extensions import NotRequired


# TODO: python 3.11 => remove total and uncomment NotRequired
class EntitySettingsType(
    TypedDict, total=False
):  # pylint: disable=too-few-public-methods
    """Base entity settings dict format."""

    object_id: str
    # object_id: NotRequired[str]


class MqttEntity:
    """MQTT base entity class."""

    _component: str = ""
    _subscriptions: dict[str, Callable[..., Any]] = {}
    _device_payload: dict[str, Any] = {}

    def __init__(
        self,
        name: str,
        unique_id: str,
        mqtt_client: mqtt.Client,
        mqtt_discovery_root_topic: str,
        mqtt_data_root_topic: str,
        logger: logging.Logger,
        device_payload: dict[str, str] | None = None,
        subscriptions: dict[str, Callable[..., Any]] | None = None,
        object_id: str | None = None,
        entity_category: str | None = None,
    ):
        """Create a new MQTT entity."""
        self._name: str = name
        self._mqtt_client = mqtt_client
        self._mqtt_discovery_root_topic = mqtt_discovery_root_topic
        self._mqtt_data_root_topic = mqtt_data_root_topic
        self._logger = logger.getChild(name)
        self._object_id = object_id
        self._entity_category = entity_category
        self._unique_id = unique_id

        if device_payload is not None:
            self._device_payload = device_payload

        if subscriptions is not None:
            self._subscriptions = subscriptions

        if not self._component:
            raise MQTTHassBaseError(
                f"Missing `_component` attributes in the class {self.__class__.name}"
            )

    def set_mqtt_client(self, mqtt_client: mqtt.Client) -> None:
        """Set MQTT client to the current entity."""
        self._mqtt_client = mqtt_client

    @property
    def component_type(self) -> str:
        """Get Entity type."""
        return self._component

    @property
    def mqtt_discovery_root_topic(self) -> str:
        """Get MQTT root topic of the entity."""
        return self._mqtt_discovery_root_topic.lower()

    @property
    def mqtt_data_root_topic(self) -> str:
        """Get MQTT root topic of data of the entity."""
        return self._mqtt_data_root_topic.lower()

    @property
    def logger(self) -> logging.Logger:
        """Get the logger of the entity."""
        return self._logger

    @property
    def name(self) -> str:
        """Get the name of the entity."""
        return self._name

    @property
    def object_id(self) -> str | None:
        """Get the object_id of the entity."""
        return self._object_id

    @property
    def entity_category(self) -> str | None:
        """Get the entity_category of the entity."""
        return self._entity_category

    @property
    def unique_id(self) -> str:
        """Get the unique_id of the entity."""
        return self._unique_id

    @property
    def device_payload(self) -> dict[str, Any]:
        """Get the device payload of the entity."""
        return self._device_payload

    @property
    def command_topic(self) -> str:
        """MQTT Command topic to receive commands from Home Assistant."""
        return "/".join(
            (self._mqtt_data_root_topic, self._component, self.name, "command")
        ).lower()

    @property
    def state_topic(self) -> str:
        """MQTT State topic to send state to Home Assistant."""
        return "/".join(
            (self._mqtt_data_root_topic, self._component, self.name, "state")
        ).lower()

    @property
    def availability_topic(self) -> str:
        """MQTT availability topic to send entity availability to Home Assistant."""
        return "/".join(
            (self._mqtt_data_root_topic, self._component, self.name, "availability")
        ).lower()

    @property
    def json_attributes_topic(self) -> str:
        """MQTT attributes topic to send attribute dict to Home Assistant."""
        return "/".join(
            (self._mqtt_data_root_topic, self._component, self.name, "attributes")
        ).lower()

    @property
    def config_topic(self) -> str:
        """Return MQTT config topic."""
        return "/".join(
            (
                self.mqtt_discovery_root_topic,
                self._component,
                self.unique_id.lower().replace(" ", "_"),
                "config",
            )
        ).lower()

    async def _on_messages(
        self,
        messages: AsyncGenerator[paho.MQTTMessage, None],
        on_message_callback: Callable[..., Any],
    ) -> None:
        """on_command MQTT callback."""
        try:
            async for message in messages:
                await on_message_callback(message)
        except mqtt.MqttError as exp:
            self.logger.warning(exp)

    async def send_available(self) -> None:
        """Set the availability to ON."""
        await self._mqtt_client.publish(
            topic=self.availability_topic, retain=True, payload="online"
        )

    async def send_not_available(self) -> None:
        """Set the availability to OFF."""
        await self._mqtt_client.publish(
            topic=self.availability_topic, retain=True, payload="offline"
        )

    async def register(self) -> None:
        """Register the current entity to Hass.

        Using the MQTT discovery feature of Home Assistant.
        """
        raise NotImplementedError

    async def subscribe(self, stack: AsyncExitStack) -> set[asyncio.Task[None]]:
        """Subscribe to all mqtt topics needed."""
        raise NotImplementedError

    async def unregister(self) -> None:
        """Unregister the current entity to Hass.

        Using the MQTT discovery feature of Home Assistant.
        """
        self.logger.info("Deleting %s: %s", self.config_topic, json.dumps({}))
        await self._mqtt_client.publish(
            topic=self.config_topic, retain=False, payload=None
        )

    async def send_state(
        self,
        state: str | bytes | float | int,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """Send current state to MQTT."""
        raise NotImplementedError

    async def send_attributes(self, attributes: dict[str, Any] | None) -> None:
        """Send current attribute dict to MQTT."""
        if attributes in (None, {}):
            return
        if not isinstance(attributes, dict):
            raise ValueError("'attributes' argument should be a dict.")
        await self._mqtt_client.publish(
            topic=self.json_attributes_topic,
            retain=True,
            payload=json.dumps(attributes),
        )
