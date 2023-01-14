"""MQTT Sensor entity module."""
import asyncio
import json
import logging
from contextlib import AsyncExitStack
from typing import Any

import asyncio_mqtt as mqtt

from mqtt_hass_base.const import SENSOR_DEVICE_CLASSES
from mqtt_hass_base.entity.common import EntitySettingsType, MqttEntity
from mqtt_hass_base.error import MQTTHassBaseError


class SensorSettingsType(
    EntitySettingsType, total=False
):  # pylint: disable=too-few-public-methods
    """Sensor entity settings dict format."""

    device_class: str | None
    expire_after: int | None
    force_update: bool | None
    off_delay: int | None
    icon: str
    unit: str
    state_class: str | None


class MqttSensor(MqttEntity):
    """MQTT Sensor entity class."""

    _component = "sensor"

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        unique_id: str,
        mqtt_client: mqtt.Client,
        mqtt_discovery_root_topic: str,
        mqtt_data_root_topic: str,
        logger: logging.Logger,
        device_payload: dict[str, str],
        subscriptions: dict[str, str],
        device_class: str | None = None,
        expire_after: int = 0,
        force_update: bool = False,
        icon: str = "",
        unit: str = "",
        state_class: str | None = None,
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
            object_id=object_id,
            entity_category=entity_category,
        )
        if device_class is not None and device_class not in SENSOR_DEVICE_CLASSES:
            msg = (
                f"Bad device class {device_class}. Should be in {SENSOR_DEVICE_CLASSES}"
            )
            self.logger.error(msg)
            raise MQTTHassBaseError(msg)
        self._device_class = device_class
        self._expire_after = expire_after
        self._force_update = force_update
        self._state_class = state_class
        self._icon = icon
        self._unit = unit

    async def register(self) -> None:
        """Register the current entity to Home Assistant.

        Using the MQTT discovery feature of Home Assistant.
        """
        config_payload = {
            "availability_topic": self.availability_topic,
            "device": self.device_payload,
            "expire_after": self._expire_after,
            "force_update": self._force_update,
            # "json_attributes_template": "",
            "json_attributes_topic": self.json_attributes_topic,
            "name": self.name,
            "payload_available": "online",
            "payload_not_available": "offline",
            "qos": 0,
            "state_topic": self.state_topic,
            "unique_id": self._unique_id,
        }
        if self._device_class:
            config_payload["device_class"] = self._device_class
        if self._state_class:
            config_payload["state_class"] = self._state_class
        if self._icon:
            config_payload["icon"] = self._icon
        if self._unit:
            config_payload["unit_of_measurement"] = self._unit
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
        return set()

    async def send_state(
        self,
        state: str | bytes | float | int,
        attributes: dict[str, Any] | None = None,
    ) -> None:
        """Send the current state of the sensor to Home Assistant."""
        if isinstance(state, (bytes, str)):
            state = state[:255]
        await self._mqtt_client.publish(
            topic=self.state_topic, retain=True, payload=state
        )
        await self.send_attributes(attributes)
